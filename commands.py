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
import requests
import AortaTools
from math import ceil
from bs4 import BeautifulSoup
from urllib.request import urlopen


def chan_msg(s, message):
    s.send("PRIVMSG #{} :{}".format(settings.CHANNEL, message))
# ----------------------------------------------------------------


def command_restart(s, *params):
    username = params[0]
    if username in settings.PRIVILEGED:
        chan_msg(s, "Hereby, I'm sentenced to death. Good bye, cruel world!")
        chan_msg(s, "/me going offline.")
        sys.exit(0)
    else:
        chan_msg(s, "Sorry, only {} can do that".format(settings.OWNER))
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
    if len(params[2]) > 0:
        if username in settings.PRIVILEGED:
            username = " ".join(params[2])
    chatter = db.get_chatter(username)
    db.close()
    if chatter:
        money = chatter['money']
        chan_msg(s, "{} you've got {} {}".format(username, money, settings.LOYALTY_CURRENCY))
    else:
        chan_msg(s, "{} nie mam Cię w bazie. Spróbuj ponownie na ok. minutę.".format(username.title()))
# ----------------------------------------------------------------


def command_przekaz(s, *params):
    username = params[0]
    if len(params[2]) > 1:
        db = AortaDatabase()
        try:
            target = params[2][0]
            amount = int(params[2][1])
            real_amount = ceil(amount + (0.1 * amount))
            chatter = db.get_chatter(username)
            print(username, amount, target)
            if chatter['money'] >= real_amount:
                target_chatter = db.get_chatter(target)
                if target_chatter:
                    print(real_amount, chatter, target_chatter)
                    db.add_money(target_chatter, amount)
                    db.remove_money(chatter, real_amount)
                    cost = real_amount - amount
                    chan_msg(s, "{} oddaje {} {} na rzecz {}. Transakcja kosztowała {} {}".format(username.title(), amount, settings.LOYALTY_CURRENCY, target.title(), cost, settings.LOYALTY_CURRENCY))
        except:
            print("wysralo sie ....")
            pass
        finally:
            db.close()
    else:
        chan_msg(s, "{} tak to się robi: !przekaz <nick> <kwota>".format(username.title()))
# ----------------------------------------------------------------


# def command_status(s, *params):
#     username = params[0]
#     if username in settings.PRIVILEGED:
#         if len(params[2]) > 0:
#             db = AortaDatabase()
#             target = params[2][0]
#             chatter = db.get_chatter(target)
#             if chatter:
#                 chan_msg(s, "{} ma w tej chwili {} {}.".format(chatter['nick'], chatter['money'], settings.LOYALTY_CURRENCY))
#             db.close()
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
        else:
            chan_msg(s, "{} tak to się robi: !bonus <nick> <kwota>".format(username.title()))
    else:
        chan_msg(s, "Sorry {} nie masz odpowiednich uprawnień.".format(username.title()))
# ----------------------------------------------------------------


def command_bonusall(s, *params):
    username = params[0]
    if username in settings.PRIVILEGED:
        if len(params[2]) > 0:
            try:
                amount = int(params[2][0])
                db = AortaDatabase()
                online_nicks = AortaTools.get_online_chatters()
                for nick in online_nicks:
                    chatter = db.get_chatter(nick)
                    if chatter:
                        db.add_money(chatter, amount)
                print('******* online nicks****************')
                print(online_nicks)
                print('******* online nicks****************')
                chan_msg(s, "Bonus dla wszystkich w postaci {} {}!".format(amount, settings.LOYALTY_CURRENCY))
            except:
                pass
            finally:
                db.close()
        else:
            chan_msg(s, "{} tak to się robi: !bonusall <kwota>".format(username.title()))
    else:
        chan_msg(s, "Sorry {} nie masz odpowiednich uprawnień.".format(username.title()))
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
                icons = ['Kappa', 'Kreygasm', 'MingLee', 'Keepo', 'NotLikeThis']
                icon = random.choice(icons)
                chan_msg(s, "{} {} {}".format(target, wypowiedz, icon))
                db.remove_money(chatter, settings.bluzgi_price)
            else:
                chan_msg(s, "Sorry, {}. Potrzebujesz {} {} by bluzgać innych!".format(username, settings.bluzgi_price, settings.LOYALTY_CURRENCY))
        else:
            print("-- Didn't find online user called {}".format(username))
        db.close()
    else:
            chan_msg(s, "{}, spróbuj tak: !zbluzgaj <nick>. Bluzganie kosztuje {} {}".format(username, settings.bluzgi_price, settings.LOYALTY_CURRENCY))
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
            if delta.days > 0:
                if delta.days == 1:
                    days = "dzień"
                else:
                    days = "dni"
                txt = "Krążą słuchy, że {} widziano tutaj ostatnio {} {} temu.".format(chatter['nick'].title(), delta.days, days)
            else:
                txt = "Najnowsze doniesienia sugerują, że widziano {} jeszcze dzisiaj jakieś ".format(chatter['nick'].title())
                if delta.seconds >= 3600:
                    txt += "{} godzin temu!".format(delta.seconds // 3600)
                elif delta.seconds < 3600 and delta.seconds > 120:
                    txt += "{} minut temu!".format(delta.seconds // 60)
                else:
                    txt = "Wygląda na to, że {} jest online właśnie teraz! 4Head".format(chatter['nick'].title())
            chan_msg(s, txt)
        else:
            chan_msg(s, "Niestety, nigdy w życiu nie widziałem tutaj {}.".format(" ".join(params[2]).title()))
        db.close()
    else:
        chan_msg(s, "{} tak to się robi: !gdzie <nick>".format(username.title()))
# ----------------------------------------------------------------


def command_gamble(s, *params):
    username = params[0]
    txt = ""
    online_nicks = AortaTools.get_online_chatters()
    if settings.CHANNEL in online_nicks:
        chan_msg(s, "{} wygląda na to, że stream jest online. Zakaz gamblowania podczas streamu do odwołania!".format(username))
        return
    if len(params[2]) > 0:
        try:
            amount = abs(int(params[2][0]))
        except:
            return
        result = random.randint(1, 100)
        db = AortaDatabase()
        chatter = db.get_chatter(username)
        if int(chatter['money']) >= amount:
            if result <= 50:
                txt = "Wylosowano {}. {} traci {} {}".format(result, username, amount, settings.LOYALTY_CURRENCY)
                amount = -amount
            elif result > 50 and result < 85:
                txt = "Wylosowano {}. {} wygrywa {} {}".format(result, username, amount, settings.LOYALTY_CURRENCY)
            elif result >= 85:
                amount = amount * 2
                txt = "Wylosowano {}. {} wygrywa {} {}".format(result, username, amount, settings.LOYALTY_CURRENCY)
            current_money = int(chatter['money']) + amount
            txt += " i ma teraz {} bullets.".format(current_money)
            db.add_money(chatter, amount)
            chan_msg(s, txt)
            db.close()
    else:
        chan_msg(s, "{} tak to się robi: !gamble <kwota>".format(username.title()))
# ----------------------------------------------------------------


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
            txt = "Sorry {} lepiej będzie, jak sobie odpuścisz. Szanse na miłość między Tobą a {} wynoszą zaledwie {}%".format(username, " ".join(params[2]).title(), love_meter)
        if love_meter > 50 and love_meter < 75:
            txt = "{} między Tobą a {} jest chemia. Podkręć bajerę i uderzaj ;) Wasze szanse wynoszą {}%".format(username, " ".join(params[2]).title(), love_meter)
        if love_meter >= 75:
            txt = "{} to prawdziwa miłość! Czym prędzej umów się z {} i róbcie dzieci! Macie {}% szans!".format(username, " ".join(params[2]).title(), love_meter)
        chan_msg(s, txt)
    else:
        chan_msg(s, "{} tak to się robi: !love <nick>".format(username.title()))
# ----------------------------------------------------------------


def command_drzewa(s, *params):
    response = requests.get(settings.WOT_API_STATS)
    if response:
        r = response.json()
        wot_user = r['data'][str(settings.WOT_USER_ID)]
        stats = wot_user['statistics']
        trees_count = stats['trees_cut']
        noun = "drzew"
        chan_msg(s, "Do tej pory {} ścięła {} {}.".format(wot_user['nickname'], trees_count, noun))
# ----------------------------------------------------------------


def command_ostatniagra(s, *params):
    response = requests.get(settings.WOT_API_STATS)
    if response:
        r = response.json()
        wot_user = r['data'][str(settings.WOT_USER_ID)]
        epoch = wot_user['last_battle_time']
        last_game = datetime.datetime.fromtimestamp(float(epoch))
        fmt = "%Y-%m-%d o %H:%M:%S"
        chan_msg(s, "Ostatnia rozgrywka w WOT odbyła się dnia {}".format(last_game.strftime(fmt)))
# ----------------------------------------------------------------


def command_kills(s, *params):
    response = requests.get(settings.WOT_API_STATS)
    if response:
        r = response.json()
        wot_user = r['data'][str(settings.WOT_USER_ID)]
        stats = wot_user['statistics']['all']
        chan_msg(s, "{} zestrzeliła do tej pory {} czołgów!".format(wot_user['nickname'], stats['frags']))
# ----------------------------------------------------------------


def command_pogoda(s, *params):
    if len(params[2]) > 0:
        city = "%20".join(params[2])
        url = 'http://api.openweathermap.org/data/2.5/weather?APPID=4614128747f3b43fb338644febb99eed&q={}'.format(city)
        city_response = requests.get(url)
        r = city_response.json()
        if r['cod'] == 200:
            w = {}
            w['temp'] = "{:.2f}".format(float(r['main']['temp'])-272.15)
            w['pressure'] = r['main']['pressure']
            w['wind_speed'] = r['wind']['speed']
            w['clouds'] = r['clouds']['all']
            w['city'] = r['name']
            txt = [
                "Aktualna pogoda dla miasta {}:".format(w['city']),
                "temperatura: {} st.C".format(w['temp']),
                "ciśnienie: {} hPa".format(w['pressure']),
                "prędkość wiatru: {} m/s".format(w['wind_speed']),
                "zachmurzenie: {}%".format(w['clouds'])
            ]
        else:
            txt = [
                "Coś nie pykło. Kod błędu: {}. Wiadomość: {}".format(
                    r['cod'], r['message']
                )
            ]
        chan_msg(s, ", ".join(txt))
# ----------------------------------------------------------------


def command_lepa(s, *params):
    username = params[0]
    if len(params[2]) > 0:
        db = AortaDatabase()
        chatter = db.get_chatter(username)
        if chatter:
            target = " ".join(params[2])
            target_chatter = db.get_chatter(target)
            if target_chatter:
                if chatter['money'] >= settings.lepa_price:
                    hitpoints = random.randint(1, 10)
                    db.remove_money(chatter, settings.lepa_price)
                    target = target.title()
                    txt = "{} wykurwia {} lepę na ryj i trafia za {}hp w główkę.".format(username, target, hitpoints)
                    if hitpoints <= 5:
                        txt += " {} stoi dalej na nogach! Twardziel!".format(target)
                    else:
                        if hitpoints > 5 and hitpoints <= 8:
                            timeout = settings.lepa_timeout
                        if hitpoints > 8:
                            timeout = settings.lepa_ko_timeout
                        txt += " {} zostaje ogłuszony na {} sekund.".format(target, timeout)
                        s.send("PRIVMSG #{} :/timeout {} {}".format(settings.CHANNEL, target, timeout))
                    chan_msg(s, txt)
                else:
                    chan_msg(s, "Za mało hajsu. !lepa kosztuje {} {}.".format(settings.lepa_price, settings.LOYALTY_CURRENCY))
            else:
                chan_msg(s, "Nie mogę sprzedać lepy {} z powodu nieobecności osoby.".format(target))
        db.close()
    else:
        chan_msg(s, "Żeby wyjebać komuś lepę użyj: !lepa <nick>")
# ----------------------------------------------------------------


def command_pupeczka(s, *params):
    username = params[0]
    db = AortaDatabase()
    chatter = db.get_chatter(username)
    if chatter:
        if chatter['money'] >= settings.nudes_price:
            db.remove_money(chatter, settings.nudes_price)
            url = random.choice(settings.NUDES_URL)
            soup = BeautifulSoup(urlopen(url), 'html.parser')
            tmp = soup.find_all('img')
            for t in tmp:
                if '.jpg' in t['src']:
                    chan_msg(s, '{} proszę bardzo, pupeczka dla Ciebie za jedyne {} {}: {}'.format(username.title(), settings.nudes_price, settings.LOYALTY_CURRENCY, t['src']))
                    break
        else:
            chan_msg(s, "Sorry {}. Za nudeski trzeba bulić {} {}".format(username, settings.nudes_price, settings.LOYALTY_CURRENCY))


def command_status(s, *params):
    online_nicks = AortaTools.get_online_chatters()
    if settings.CHANNEL in online_nicks:
        txt = "Broadcaster {} online. FeelsAmaizingMan".format(settings.CHANNEL)
    else:
        txt = "Broadcaster {} is offline. FeelsBadMan".format(settings.CHANNEL)
    chan_msg(s, txt)


def command_user(s, *params):
    username = params[0]
    if len(params[2]) > 0:
        tocheck = " ".join(params[2])
        user = AortaTools.get_twitch_user_info(tocheck)
        if user:
            chan_msg(s, "{} user ID: {}".format(tocheck, user['id']))
        else:
            chan_msg("Cos sie spierdolilo.. {}: {}".format(tocheck, user))


def command_follow(s, *params):
    username = params[0]
    bnick = settings.CHANNEL
    if len(params[2]) > 0:
        bnick = " ".join(params[2])
    broadcaster = AortaTools.get_twitch_user_info(bnick)
    user = AortaTools.get_twitch_user_info(username)
    if broadcaster and user:
        response = AortaTools.get_twitch_follow_time(user['id'], broadcaster['id'])
        if response:
            today = datetime.datetime.now()
            date = datetime.datetime.strptime(response['followed_at'],
                                              "%Y-%m-%dT%H:%M:%SZ")
            delta = today - date
            chan_msg(s, "Follow od {} dni".format(delta.days))
    else:
        chan_msg(s, "Spierdoliłoś:{}:{}".format(user, broadcaster))
