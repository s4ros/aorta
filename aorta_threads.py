import threading
import sys
import time
import requests
import settings
import json
import queue

from database import AortaDatabase

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------


class ReceiverThread(threading.Thread):
    """ Thread - receiver, receives Twitch IRC communicates"""
    def __init__(self, sock, queue):
        threading.Thread.__init__(self)
        self.setName('ReceiverThread')
        self.s = sock
        self.q = queue
        self.buffer = ""

    def run(self):
        while True:
            try:
                # stringdata = data.decode('utf-8')
                self.buffer = self.buffer + self.s.recv(1024).decode('utf-8')
                txt = str.split(self.buffer, "\r\n")
                print(self.name, txt)
                self.buffer = txt.pop()
                for line in txt:
                    if line == "PING :tmi.twitch.tv":
                        print('::PING::PONG::')
                        self.s.send("PONG :tmi.twitch.tv")
                    self.q.put(line.lower())
            except:
                print("xxx ReceiverThread sie wysypal")
                print(sys.exc_info()[0])
                # sys.exit(1)
                pass


class LoyaltyPointsThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setName('LoyaltyPointsThread')
        self.time_passed = 0
        self.chatters_url = "http://tmi.twitch.tv/group/user/{}/chatters".format(settings.CHANNEL)
        self.online_nicks = []

    def get_online_chatters(self):
        self.online_nicks = []
        r = requests.get(self.chatters_url)
        chatters = json.loads(r.content)
        chatters = chatters['chatters']
        people_cat = ['moderators', 'viewers']
        for pc in people_cat:
            for p in chatters[pc]:
                # print("get_online_chatters - {}".format(p))
                self.online_nicks.append(p)

    def add_loyalty_points(self):
        db = AortaDatabase()
        # get all users from db
        self.database_chatters = db.get_chatters()
        self.get_online_chatters()
        db_nicks = []
        try:
            for nick in self.database_chatters:
                db_nicks.append(nick['nick'])
            # adding new users to db
            for c in self.online_nicks:
                if c not in db_nicks:
                    # print("----------------===========> Added chatter with nick: {} ".format(c))
                    db.add_chatter(c)
            # add money to all online users
            for nick in self.online_nicks:
                if nick in [settings.NICK, settings.CHANNEL]:
                    continue
                chatter = db.get_chatter(nick)
                db.add_money(chatter, settings.LOYALTY_POINTS)
                db.update_last_seen(chatter)
        except:
            print("Unfortunately, no users in queue or smth.")
            pass
        db.close()

    def run(self):
        while True:
            self.time_passed += 1
            if (self.time_passed % settings.LOYALTY_INTERVAL) == 0:
                print("{} seconds have passed".format(settings.LOYALTY_INTERVAL))
                self.add_loyalty_points()
                print("*" * 25)
                self.time = 0
            time.sleep(1)


class AortaDatabaseProcessor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setName('AortaDatabaseProcessor')
        self.queue = queue.Queue()

    def run(self):
        while True:
            try:
                query = self.queue.get(timeout=0.2)
                if query:
                    db = AortaDatabase()
                    db.process_query(query)
                    db.close()
                    time.sleep(0.1)
            except queue.Empty:
                pass
