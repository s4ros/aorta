# -*- coding: utf-8 -*-
# settings.py file for AortaBOT.py bot
# those settings probably won't work :)

# Twitch IRC server address
HOST = 'irc.chat.twitch.tv'
# Twitch IRC server port
PORT = 6667
# Your Bot's nickname that will be displayed on Userlist
# In most cases it's your twitch login
NICK = 'bot_nickname'
# oauth secret key that can be obtained on
# http://www.twitchapps.com/tmi/
PASS = 'oauth:youroauthsecretkey'
# your channel - twitch name
CHANNEL = 'channel'
# Channel owner/streamer nickname (probably the same as CHANNEL)
OWNER = 'your_nick'

# list of privileged users to use commands like !halt, !bonus, etc.
PRIVILEGED = [
    'sarosiak',
    'aortabot',
    'aorta_bot'
]

# interval time in seconds
LOYALTY_INTERVAL = 10
# how many points will be added when INTERVAL will pass
LOYALTY_POINTS = 100
# the uber name of your own Currency
LOYALTY_CURRENCY = "Hajsy"

# path to the sqlite3 database file
DATABASE = 'aorta_www/db.sqlite3'

ruletka_price = 15
ruletka_win = 100
bluzgi_price = 5

# ads
adv = True         # True/False - if False, advertising is disabled
adv_step = 30
adv_fb = 'https://facebook.com/AortaBOT'
adv_twitter = 'https://twitter.com/AortaBOT'
adverts = [
    "Witam na kanale #{}! Zapraszam do śledzenia FB-{} / Twitter-{} czy cokolwiek".format(CHANNEL, adv_fb, adv_twitter),
    "Super randomowa reklama #2",
    "Jakis inny randomowy tekst, ktorym bot bedzie przemawial od czasu do czasu #3"
]

# you should use your own local_settings.py settings
try:
    from local_settings import *
except:
    pass
