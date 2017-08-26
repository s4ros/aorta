# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Commands - serve commands detected in IRC channel
# ----------------------------------------------------------------------------

import settings
import sys
import random
from database import AortaDatabase


def chan_msg(s, message):
    s.send("PRIVMSG #{} :{}".format(settings.CHANNEL, message))
# ----------------------------------------------------------------


def command_halt(s, *params):
    username = params[0]
    if username == settings.OWNER:
        chan_msg(s, "Hereby, I'm sentenced to death. Good bye, cruel world!")
        chan_msg(s, "/me going offline.")
        sys.exit(0)
    else:
        chan_msg(s, "Sorry, only {} can do that".format(settings.OWNER))
# ----------------------------------------------------------------


def command_test(s, *params):
    username = params[0]
    chan_msg(s, "Hello {}! It's a successful test command execution.".format(username))
# ----------------------------------------------------------------


def command_ruletka(s, *params):
    username = params[0]
    db = AortaDatabase()
    chatter = db.get_chatter(username)
    number_user = random.randint(1, 6)
    number_gun = random.randint(1, 6)
    txt = "{} zakręca bębenek...".format(username)
    if number_user == number_gun:
        txt = txt + " JEB! {} umiera w powolnej i okrutnej agonii.".format(username)
        db.remove_money(chatter, 500)
    else:
        txt = txt + " KLIK.. Bębenek był pusty - {} tym razem miałeś fuksa.".format(username)
        db.remove_money(chatter, 100)
    db.close()
    chan_msg(s, txt)
# ----------------------------------------------------------------


def command_commands(s, *params):
    commands = {}
    for key, value in globals().items():
        if key.startswith("command_"):
            commands[key[8:]] = value
    txt = ""
    for cmd in commands:
        txt += "!{}, ".format(cmd)
    chan_msg(s, "Dostępne polecenia: " + txt)
# ----------------------------------------------------------------


def command_points(s, *params):
    username = params[0]
    db = AortaDatabase()
    chatter = db.get_chatter(username)
    db.close()
    money = chatter['money']
    chan_msg(s, "{} użytkownika {}: {}".format(settings.LOYALTY_CURRENCY, username, money))
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
