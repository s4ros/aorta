# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Commands - serve commands detected in IRC channel
# ----------------------------------------------------------------------------

import settings
import sys
import random

def chan_msg(s, message):
    s.send("PRIVMSG #{} :{}".format(settings.CHANNEL, message))

# ----------------------------------------------------------------
def command_halt(s, *params):
    """
    !halt - shutdown the bot
    """
    chan_msg(s, "Hereby, I'm sentenced to death. Good bye, cruel world!")
    sys.exit(0)
# ----------------------------------------------------------------
def command_test(s, *params):
    username = params[0]
    chan_msg(s,"Hello {}! It's a successful test command execution.".format(username))
    pass
# ----------------------------------------------------------------
def command_ruletka(s, *params):
    username = params[0]
    number_user = random.randint(1,6)
    number_gun = random.randint(1,6)
    txt = "{} zakręca bębenek...".format(username)
    if number_user == number_gun:
        txt=txt+" JEB! {} umiera w powolnej i okrutnej agonii.".format(username)
    else:
        txt=txt+" KLIK.. Bębenek był pusty. {} żyje dalej.".format(username)
    chan_msg(s, txt)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
