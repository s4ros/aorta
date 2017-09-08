# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Commands - serve commands detected in IRC channel
# ----------------------------------------------------------------------------

import settings
import sys
import random
from database import AortaDatabase
import json


def chan_msg(s, message):
    s.send("PRIVMSG #{} :{}".format(settings.CHANNEL, message))
# ----------------------------------------------------------------


def command_halt(s, *params):
    username = params[0]
    if username in settings.PRIVILEGED:
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
    if chatter['money'] >= settings.ruletka_cost:
        number_user = random.randint(1, 10)
        number_gun = random.randint(1, 10)
        txt = "{} is spinning the cylinder...".format(username)
        if number_user != number_gun:
            txt = txt + " BANG! {} dies in slow and painful agony. You lost {} {}".format(username, settings.ruletka_cost, settings.LOYALTY_CURRENCY)
            db.remove_money(chatter, settings.ruletka_cost)
        else:
            txt = txt + " *CLICK*.. Lucky you {}. Gun chamber was empty.. this time. You earned {} {}".format(username, settings.ruletka_win, settings.LOYALTY_CURRENCY)
            db.add_money(chatter, settings.ruletka_win)
    else:
        txt = "Sorry {}, don't have enough {}. Spinning the cylinder costs {} {}".format(username, settings.LOYALTY_CURRENCY, settings.ruletka_cost, settings.LOYALTY_CURRENCY)
    db.close()
    chan_msg(s, txt)
# ----------------------------------------------------------------


def command_help(s, *params):
    commands = {}
    for key, value in globals().items():
        if key.startswith("command_"):
            commands[key[8:]] = value
    txt = ""
    for cmd in commands:
        txt += "!{}, ".format(cmd)
    chan_msg(s, "Dostępne polecenia: " + txt)
# ----------------------------------------------------------------


def command_bullets(s, *params):
    username = params[0]
    db = AortaDatabase()
    chatter = db.get_chatter(username)
    db.close()
    money = chatter['money']
    chan_msg(s, "{}, you've got {} {}".format(username, money, settings.LOYALTY_CURRENCY))


def command_bonus(s, *params):
    username = params[0]
    target = params[2][0]
    amount = params[2][1]
    if username in settings.PRIVILEGED:
        db = AortaDatabase()
        chatter = db.get_chatter(target)
        if chatter:
            db.add_money(chatter, amount)
            chan_msg(s, "{} receives additional {} {}".format(target, amount, settings.LOYALTY_CURRENCY))
# ----------------------------------------------------------------


def command_zbluzgaj(s, *params):
    username = params[0]
    if len(params[2]) > 0:
        db = AortaDatabase()
        chatter = db.get_chatter(username)
        if chatter['money'] >= settings.bluzgi_price:
            bluzgi = json.load(open('bluzgi.json', 'r'))
            target = params[2][0]
            bluzg = bluzgi[random.randint(0, len(bluzgi))]
            wypowiedz = bluzg['sentence'].format(target)
            chan_msg(s, "{} {}".format(target, wypowiedz))
            db.remove_money(chatter, settings.bluzgi_price)
        else:
            chan_msg(s, "Sorry, {}. Potrzebujesz {} {} by bluzgać innych!".format(username, settings.bluzgi_price, settings.LOYALTY_CURRENCY))
    else:
            chan_msg(s, "{}, spróbuj tak: !zbluzgaj <nick>".format(username))
    print("-------- bluzgaj -------")
# ----------------------------------------------------------------
# ----------------------------------------------------------------
