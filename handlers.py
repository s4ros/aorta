# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Handlers - serve detected events
# ----------------------------------------------------------------------------

import settings
import random
import time
from commands import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
from decorators import static_vars
import logging

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------

# bot commands initialization function
commands = {}


def init_commands(commands):
    for key, value in globals().items():
        if key.startswith("command_"):
            commands[key[8:]] = value
            logger.debug("New command registered: {} = {}".format(key, value))

# ----------------------------------------------------------------


def handle_376(s, *params):
    """
    Event 376 occurs when successfuly authenticated into IRC service.
    """
    s.send("JOIN #{}".format(settings.CHANNEL))
    s.send("CAP REQ :twitch.tv/membership")
    s.send("CAP REQ :twitch.tv/tags")
    s.send("CAP REQ :twitch.tv/commands")
    init_commands(commands)

# ----------------------------------------------------------------


def handle_cap(s, *params):
    """
    CAP ACK events are sent in response to CAP REQ.
    """
    pass

# ----------------------------------------------------------------


# ----------------------------------------------------------------


def handle_join(s, *params):
    username = params[0][1:].split('!')[0]
    if username.lower() == settings.NICK:
        logger.debug("Welcome message sent.")
        s.send("PRIVMSG #{} :/me is online!\r\n".format(settings.CHANNEL))

# ----------------------------------------------------------------


def handle_part(s, *params):
    pass

# ----------------------------------------------------------------


@static_vars(counter=0)
def handle_privmsg(s, *params):
    handle_privmsg.counter += 1
    if settings.adv:
        if handle_privmsg.counter >= settings.adv_step:
            # num = random.randint(0, len(settings.adverts) - 1)
            # print("\n::::: NUM ::::: {} ::::::".format(num))
            # s.send("PRIVMSG #{} :{}".format(settings.CHANNEL, settings.adverts[num]))
            handle_privmsg.counter = 0
    username = params[1].split('!', 1)[0][1:]
    text = params[3].split(':', 1)[1]
    badges = params[0][8:].split(';', 1)[0]
    logger.info("[{}]> {}".format(username, text))
    if text[0] == '!':
        cmd = text.split(' ', 1)[0]
        cmd = cmd[1:]
        others = text.split(' ', 2)[1:]
        params = (username, cmd, others)
        if cmd in commands:
            commands[cmd](s, *params)
            time.sleep(0.3)
        else:
            if (handle_privmsg.counter % 5) == 0:
                command_help(s, *params)
    if 'http://' in text or 'https://' in text:
        url = text.split(' ', 1)[0]
        print("===== ULR TO OPEN: {}".format(url))
        try:
            soup = BeautifulSoup(urlopen(url), "html.parser")
            if soup.title:
                logger.info('Url catched: {}'.format(soup.title.text))
                title = u''.join(soup.title.text)
                s.send(u"PRIVMSG #{} :{} - {}".format(settings.CHANNEL, url, title))
        except:
            print("=/=/=/=/=/= ULR {} didn't open. Exception.".format(url))
            pass

# ----------------------------------------------------------------


def handle_usernotice(s, *params):
    """
    @badges=subscriber/0,premium/1;color=#19B34A;display-name=Nimanski;emotes=;id=5b3968b0-19c5-46cf-bf1a-28eff7c83d41;login=nimanski;mod=0;msg-id=resub;msg-param-months=2;msg-param-sub-plan-name=Dr\sDisRespect;msg-param-sub-plan=Prime;room-id=17337557;subscriber=1;system-msg=Nimanski\sjust\ssubscribed\swith\sTwitch\sPrime.\sNimanski\ssubscribed\sfor\s2\smonths\sin\sa\srow!;tmi-sent-ts=1498078543927;turbo=0;user-id=69832970;user-type= :tmi.twitch.tv USERNOTICE #drdisrespectlive :Go Doc, keep dominating these blonde banged snot nosed punks! yeahyeahyeahyeahyeahyeahyeahyeahyeahyeahyeahyeah.. RAAAUULLLLLLLLLL!
"""
    print("::::::USERNOTICE::params::{}".format(params))
    ######## useful shit
    # display-name=Nimanski
    # login=nimanski
    # msg-id=resub
    # msg-param-months=2
    # system-msg=Nimanski\sjust\ssubscribed\swith\sTwitch\sPrime.\sNimanski\ssubscribed\sfor\s2\smonths\sin\sa\srow!
    pass


def handle_userstate(s, *params):
    print(":::::USERSTATE::params::{}".format(params))
