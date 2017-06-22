import threading
import string
import sys
import time

# ----------------------------------------------------------------------------
# Thread - receiver, receives Twitch IRC communicates
# ----------------------------------------------------------------------------
class ReceiverThread(threading.Thread):
  def __init__(self, sock, queue):
    threading.Thread.__init__(self)
    self.s = sock
    self.q = queue
    self.buffer = ""

  def run(self):
    while True:
        try:
            self.buffer = self.buffer + self.s.recv(1024)
            txt = string.split(self.buffer, "\n")
            self.buffer = txt.pop()
            for line in txt:
                line = line[:-1]
                if line == "PING :tmi.twitch.tv":
                    self.s.sendall("PONG :tmi.twitch.tv\r\n")
                    continue
                self.q.put(line)
        except:
            print "xxx ReceiverThread sie wysypal"
            sys.exit(1)
