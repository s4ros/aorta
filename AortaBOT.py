#
# AortaBOT
#  (c) by s4ros
#

import socket
import sys
import time
import queue
import random

from aorta_threads import ReceiverThread, LoyaltyPointsThread

# import settings
import settings

# import handlers
from handlers import *

# import database class
from database import AortaDatabase

import logging

logging.basicConfig(
    format='%(asctime)s|%(name)s.%(funcName)s|%(levelname)s|%(message)s',
    datefmt='%s',
    level=logging.DEBUG
)

# create logger
logger = logging.getLogger(__name__)


class asocket(object):
    def __init__(self, *param):
        self._socket = socket.socket(*param)

    def __getattr__(self, name):
        return getattr(self._socket, name)

    def send(self, txt):
        time.sleep(0.2)
        self._socket.sendall(bytes(txt + "\r\n", "utf-8"))

# ----------------------------------------------------------------------------


class AortaBOT(object):
    # ---
    def __init__(self):
        self.handlers = {}
        self.init_handlers()
        self.queue = queue.Queue()
    # ---

    def init_rng(self):
        random.seed()

    def init_handlers(self):
        for key, value in list(globals().items()):
            if key.startswith("handle_"):
                self.handlers[key[7:]] = value
                logger.info("New handler registered: {} = {}".format(key, value))
    # ---

    def init_socket(self):
        try:
            self._socket = asocket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((settings.HOST, settings.PORT))
            logger.debug("Sockets initialized")
        except:
            logger.critical("socket/connection failed")
            sys.exit(1)
    # ---

    def init_threads(self):
        self.rt = ReceiverThread(self._socket, self.queue)
        self.rt.daemon = True
        self.rt.start()

        self.lpt = LoyaltyPointsThread()
        self.lpt.daemon = True
        self.lpt.start()
    # ---

    def say_hello(self):
        self._socket.send("PASS {}".format(settings.PASS))
        self._socket.send("NICK {}".format(settings.NICK))
    # ---

    def run(self):
        logger.info("AortaBOT is running")
        self.init_rng()
        self.init_socket()
        self.init_threads()
        self.say_hello()
        while True:
            try:
                msg = self.queue.get()
                action = ""
                params = ""
                if msg[0] == ':':
                    who, action, content = msg.split(' ', 2)
                    params = (who, action, content)
                elif msg[0] == '@':
                    badges, who, action, content = msg.split(' ', 3)
                    params = (badges, who, action, content)
                else:
                    pass
                print("\n")
                if action in self.handlers:
                    logger.info('Hanlder action for {} trigerred.'.format(action))
                    self.handlers[action](self._socket, *params)
                else:
                    logger.warning('No handler found for {}'.format(action))
            except queue.Empty:
                pass


if __name__ == "__main__":
    bot = AortaBOT()
    bot.run()
