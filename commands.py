# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Commands - serve commands detected in IRC channel
# ----------------------------------------------------------------------------

import settings
import sys
import random
from database import AortaDatabase
import json
import datetime


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


# def command_test(s, *params):
#     username = params[0]
#     chan_msg(s, "Hello {}! It's a successful test command execution.".format(username))
# ----------------------------------------------------------------


def command_ruletka(s, *params):
    username = params[0]
    db = AortaDatabase()
    chatter = db.get_chatter(username)
    if chatter['money'] >= settings.ruletka_price:
        number_user = random.randint(1, 10)
        number_gun = random.randint(1, 10)
        txt = "{} is spinning the cylinder...".format(username)
        if number_user != number_gun:
            txt = txt + " BANG! {} dies in slow and painful agony. You lost {} {}".format(username, settings.ruletka_price, settings.LOYALTY_CURRENCY)
            db.remove_money(chatter, settings.ruletka_price)
        else:
            txt = txt + " *CLICK*.. Lucky you {}. Gun chamber was empty.. this time. You earned {} {}".format(username, settings.ruletka_win, settings.LOYALTY_CURRENCY)
            db.add_money(chatter, settings.ruletka_win)
    else:
        txt = "Sorry {} you don't have enough {}. Spinning the cylinder costs {} {}".format(username, settings.LOYALTY_CURRENCY, settings.ruletka_price, settings.LOYALTY_CURRENCY)
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
    chan_msg(s, "{} you've got {} {}".format(username, money, settings.LOYALTY_CURRENCY))


def command_bonus(s, *params):
    username = params[0]
    if username in settings.PRIVILEGED:
        if len(params[2]) > 1:
            target = params[2][0]
            amount = params[2][1]
            db = AortaDatabase()
            chatter = db.get_chatter(target)
            if chatter:
                db.add_money(chatter, amount)
                chan_msg(s, "{} receives additional {} {}".format(target, amount, settings.LOYALTY_CURRENCY))
            db.close()

# ----------------------------------------------------------------


def command_zbluzgaj(s, *params):
    username = params[0]
    if len(params[2]) > 0:
        db = AortaDatabase()
        chatter = db.get_chatter(username)
        if chatter:
            if chatter['money'] >= settings.bluzgi_price:
                bluzgi = json.load(open('bluzgi.json', 'r'))
                # target = params[2][0]
                target = " ".join(params[2]).title()
                bluzg = bluzgi[random.randint(0, len(bluzgi))]
                wypowiedz = bluzg['sentence'].format(target)
                chan_msg(s, "{} {}".format(target, wypowiedz))
                db.remove_money(chatter, settings.bluzgi_price)
            else:
                chan_msg(s, "Sorry, {}. Potrzebujesz {} {} by bluzgać innych!".format(username, settings.bluzgi_price, settings.LOYALTY_CURRENCY))
        else:
            print("-- Didn't find online user called {}".format(username))
        db.close()
    else:
            chan_msg(s, "{}, spróbuj tak: !zbluzgaj <nick>. Bluzganie kosztuje {} {}".format(username, settings.bluzgi_price, settings.LOYALTY_CURRENCY))
    print("-------- bluzgaj -------")
# ----------------------------------------------------------------


def command_gdzie(s, *params):
    username = params[0]
    time_now = datetime.datetime.now()
    if len(params[2]) > 0:
        db = AortaDatabase()
        chatter = db.get_chatter(params[2][0])
        if chatter:
            last_seen = chatter['last_seen']
            delta = time_now - datetime.datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S")
            if delta.days == 1:
                days = "dzień"
            else:
                days = "dni"
            chan_msg(s, "Krążą słuchy, że {} widziano tutaj ostatnio {} {} temu.".format(chatter['nick'], delta.days, days))
        else:
            chan_msg(s, "Niestety, nigdy w życiu nie widziałem tutaj {}.".format(params[2][0]))
        db.close()
# ----------------------------------------------------------------


def command_gamble(s, *params):
    username = params[0]
    txt = ""
    if len(params[2]) > 0:
        try:
            amount = int(params[2][0])
        except:
            return
        result = random.randint(1, 100)
        db = AortaDatabase()
        chatter = db.get_chatter(username)
        if int(chatter['money']) >= amount:
            if result <= 80:
                txt = "Wylosowano {}. {} traci {} {}".format(result, username, amount, settings.LOYALTY_CURRENCY)
                amount = -amount
            elif result > 80 and result < 95:
                txt = "Wylosowano {}. {} wygrywa {} {}".format(result, username, amount, settings.LOYALTY_CURRENCY)
            elif result >= 95:
                amount = amount * 2
                txt = "Wylosowano {}. {} wygrywa {} {}".format(result, username, amount, settings.LOYALTY_CURRENCY)
            current_money = int(chatter['money']) + amount
            txt += " i ma teraz {} bullets.".format(current_money)
            db.add_money(chatter, amount)
            chan_msg(s, txt)
            db.close()


def command_love(s, *params):
    username = params[0]
    if len(params[2]) > 0:
        love = "".join(params[2])
        concat = "".join([username, love]).upper()
        concat = concat.replace(" ", "")
        love_meter = 0
        for l in concat:
            love_meter += ord(l)
        love_meter %= 101
        if love_meter <= 50:
            txt = "Sorry {} lepiej będzie, jak sobie odpuścisz. Szanse na miłość między Tobą a {} wynoszą zaledwie {}%".format(username, " ".join(params[2]), love_meter)
        if love_meter > 50 and love_meter < 75:
            txt = "{} między Tobą a {} jest chemia. Podkręć bajerę i uderzaj ;) Wasze szanse wynoszą {}%".format(username, " ".join(params[2]), love_meter)
        if love_meter >= 75:
            txt = "{} to prawdziwa miłość! Czym prędzej umów się z {} i róbcie dzieci! Macie {}% szans!".format(username, " ".join(params[2]), love_meter)
        chan_msg(s, txt)
