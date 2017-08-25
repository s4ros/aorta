import threading
import string
import sys
import time
import requests
import settings
import json

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------


class ReceiverThread(threading.Thread):
    """ Thread - receiver, receives Twitch IRC communicates"""
    def __init__(self, sock, queue):
        threading.Thread.__init__(self)
        self.s = sock
        self.q = queue
        self.buffer = ""

    def run(self):
        while True:
            try:
                # stringdata = data.decode('utf-8')
                self.buffer = self.buffer + self.s.recv(1024).decode('utf-8')
                txt = str.split(self.buffer, "\r\n")
                # print(txt)
                self.buffer = txt.pop()
                print(self.buffer)
                for line in txt:
                    if line == "PING :tmi.twitch.tv":
                        self.s.sendall("PONG :tmi.twitch.tv\r\n")
                        continue
                    self.q.put(line)
            except:
                print("xxx ReceiverThread sie wysypal")
                sys.exit(1)


class LoyaltyPointsThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.time_passed = 0
        self.chatters_url = "http://tmi.twitch.tv/group/user/{}/chatters".format(settings.CHANNEL)
        self.q = queue

    def get_chatters(self):
        self.q.queue.clear()
        r = requests.get(self.chatters_url)
        chatters = json.loads(r.content)
        chatters = chatters['chatters']
        people_cat = ['moderators', 'viewers']
        for pc in people_cat:
            for p in chatters[pc]:
                self.q.put(p)

    def add_loyalty_points(self):
        pass

    def run(self):
        while True:
            self.time_passed += 1
            if (self.time_passed % settings.LOYALTY_INTERVAL) == 0:
                self.get_chatters()
                print(list(self.q.queue))
                print("{} seconds have passed".format(settings.LOYALTY_INTERVAL))
                print("*" * 25)
            time.sleep(1)
            print("Time elapsed: {}".format(self.time_passed))
