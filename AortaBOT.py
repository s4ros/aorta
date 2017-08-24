#
# AortaBOT
#  (c) by s4ros
#

import socket
import sys
import time
import string
import Queue

from aorta_threads import ReceiverThread

# import settings
import settings

# import handlers
from handlers import *


class asocket(object):
    def __init__(self, *param):
        self._socket = socket.socket(*param)

    def __getattr__(self, name):
        return getattr(self._socket, name)

    def send(self, txt):
        time.sleep(0.2)
        self._socket.sendall(txt + "\r\n")

# ----------------------------------------------------------------------------


class AortaBOT(object):
    # ---
    def __init__(self):
        print(self)
        self.handlers = {}
        self.init_handlers()
        self.queue = Queue.Queue()
    # ---

    def init_handlers(self):
        for key, value in globals().items():
            if key.startswith("handle_"):
                self.handlers[key[7:]] = value
                print("New handler registered: {} = {}".format(key, value))
    # ---

    def init_socket(self):
        try:
            self._socket = asocket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((settings.HOST, settings.PORT))
        except:
            print("-- socket/connection failed")
            sys.exit(1)
    # ---

    def init_recv_thread(self):
        self.rt = ReceiverThread(self._socket, self.queue)
        self.rt.daemon = True
        self.rt.start()
    # ---

    def say_hello(self):
        self._socket.send("PASS {}".format(settings.PASS))
        self._socket.send("NICK P{}".format(settings.NICK))
    # ---
    # ---
    # ---

    def run(self):
        print("Running")
        self.init_socket()
        self.init_recv_thread()
        self.say_hello()
        while True:
            try:
                msg = self.queue.get(timeout=0.1)
                if msg[0] == ':':
                    who, action, content = msg.split(' ', 2)
                    params = (who, action, content)
                elif msg[0] == '@':
                    badges, who, action, content = msg.split(' ', 3)
                    params = (badges, who, action, content)
                else:
                    pass
                print("\n")
                print(params)
                if action in self.handlers:
                    self.handlers[action](self._socket, *params)
                    print("-- Handler action required: {}".format(action))
                else:
                    print("-- NO HANDLER found for {}".format(action))
                    print(msg)
                    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            except Queue.Empty:
                pass


if __name__ == "__main__":
    bot = AortaBOT()
    bot.run()
