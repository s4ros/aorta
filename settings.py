# settings.py file for aorta.py bot
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

# you should use your own local_settings.py settings
try:
    from local_settings import *
except:
    pass
