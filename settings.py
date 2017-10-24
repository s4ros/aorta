# -*- coding: utf-8 -*-
# settings.py file for AortaBOT.py bot
# those settings probably won't work :)

import os

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
CHANNEL = os.getenv('aorta_channel', 'aortabot')
# Channel owner/streamer nickname (probably the same as CHANNEL)
OWNER = 'your_nick'

# list of privileged users to use commands like !halt, !bonus, etc.
PRIVILEGED = [
    'sarosiak',
    'aortabot',
    'aorta_bot'
]

TWITCH_CLIENT_ID = os.getenv('aorta_twitch_clientid', '123456')
TWITCH_KEY = os.getenv('aorta_twitch_key', '123456')

WOT_USER_ID = os.getenv('aorta_wotid', "123456")
WOT_API_STATS = "https://api.worldoftanks.eu/wot/account/info/?application_id=demo&account_id={}".format(WOT_USER_ID)

NUDES_URL = [
    'http://sexynerdpics.tumblr.com/random',
    'https://fitsexygirls.tumblr.com/random',
    'https://ruinedgirl420.tumblr.com/random',
    'https://hot-cosplay-babes.tumblr.com/random',
    'https://aortabot.tumblr.com/random'
]

STUPKI_URL = [
    'http://nice-feet.tumblr.com/random'
]

# interval time in seconds
LOYALTY_INTERVAL = 60
# how many points will be added when INTERVAL will pass
LOYALTY_POINTS = 1
# the uber name of your own Currency
LOYALTY_CURRENCY = os.getenv('aorta_currency', "bullets")

# path to the sqlite3 database file
DATABASE = os.getenv('aorta_database', 'aorta_www/db.sqlite3')

# price for triggering !lepa
lepa_price = 10
lepa_timeout = 1
lepa_ko_timeout = 10

# price for triggering !ruletka
ruletka_price = 15
# amount of LOYALTY_POINTS that user would receive if he survived the !ruletka
ruletka_win = 100

# price for triggering !zbluzgaj
bluzgi_price = 10

# price for !sendnudes
nudes_price = 20

# ads
adv = bool(os.getenv("aorta_adv", "False"))         # True/False - if False,) advertising is disabled
adv_step = 30
# adv_fb = 'https://facebook.com/AortaBOT'
# adv_twitter = 'https://twitter.com/AortaBOT'
# adverts = [
    # "Witam na streamie! Zapraszam do śledzenia FB {}".format(adv_fb),
    # "Super randomowa reklama #2",
    # "Jakis inny randomowy tekst, ktorym bot bedzie przemawial od czasu do czasu #3",
    # "Nasza waluta to {}. Każda minuta spędzona na streamie daje Ci 1 {}. Walutę można wykorzystać do !ruletka lub !zbluzgaj. Dostępne komendy !help. Więcej funkcjonalności wkrótce :)".format(LOYALTY_CURRENCY, LOYALTY_CURRENCY),
# ]

# you should use your own local_settings.py settings
try:
    from local_settings import *
except:
    print("zesraly sie local_settings przy imporcie")
    pass
