#! /usr/bin/env python
# -*- coding: utf8 -*-


"""
  Aorta Twitch Bot - Simple bot to generate and stash #channel and users stats

  (c) by s4ros
  Infinigy Nerd Timeless Squad

  WWW.
    http://s4ros.it
    http://aorta.inifnigy.pl

  Credits goes to Joel Rosdahl for his irc Python module
  https://github.com/jaraco/irc
"""

import re
import urllib2
from BeautifulSoup import BeautifulSoup
from revlo.client import RevloClient
from ConfigParser import SafeConfigParser
import sys
# -----
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class Aorta(irc.bot.SingleServerIRCBot):
#  -------------------------------------------
  def __init__(self):
    parser = SafeConfigParser()
    try:
      parser.read('config.ini')
    except Exception, e:
      raise e("Cannot open config.ini file")

    server = parser.get('twitch', 'server')
    port = int(parser.get('twitch', 'port'))
    nickname = parser.get('twitch', 'username')
    password = parser.get('twitch', 'oauth')
    channel = parser.get('twitch', 'channel')
    api_key = parser.get('revlo', 'api_key')
    self.owner = parser.get('twitch', 'owner')

    irc.bot.SingleServerIRCBot.__init__(self, [(server,port,password)], nickname, nickname)
    self.channel = channel
    self.revlo = RevloClient(api_key)

#  -------------------------------------------
  def on_nicknameinuse(self, c, e):
    c.nick(c.get_nickname() + "_")

#  -------------------------------------------
  def on_welcome(self, c, e):
    print('event')
    print(e)
    print('-'*25)
    print('conn')
    print(dir(c))
    print('-'*25)
    print(c.__dict__)
    print('-'*25)
    c.join(self.channel)

#  -------------------------------------------
  def on_privmsg(self, c, e):
    print("on_privmsg()")
    print(e)

##  -------------------------------------------
# -- on_pubmsg()
  def on_pubmsg(self, c, e):
    print("on_pubmsg()")
    print(e)

    # get page title
    if ('https://' in e.arguments[0]) or ('http://' in e.arguments[0]):
      print(e.arguments)
      url = re.search("(?P<url>https?://[^\s]+)", e.arguments[0]).group("url")
      try:
        soup = BeautifulSoup(urllib2.urlopen(url))
      except:
        c.privmsg(self.owner, u' ↳ FATAL error during opening '+url)
        return
      if soup.title:
        # print(soup.title.string.strip('\n'))
        c.privmsg(e.target, u' ↳title: ' + ''.join(soup.title.string.strip('\n')))
      else:
        c.privmsg(e.target, u' ↳title: <Unknown>! DansGame')

# --------------------------------------------
# -- on_join()
  def on_join(self, c, e):
    print('on_join()')
    print(e)


###################
#
if __name__ == "__main__":
  bot = Aorta()
  bot.start()
