import requests
import json
import settings


def get_online_chatters():
    online_nicks = []
    chatters_url = "http://tmi.twitch.tv/group/user/{}/chatters".format(settings.CHANNEL)
    r = requests.get(chatters_url)
    chatters = json.loads(r.content)
    chatters = chatters['chatters']
    people_cat = ['moderators', 'viewers']
    for pc in people_cat:
        for p in chatters[pc]:
            online_nicks.append(p)
    return online_nicks


def get_twitch_user_info(username):
    url = 'https://api.twitch.tv/helix/users?login={}'.format(username)
    headers = {
        'Client-ID': '{}'.format(settings.TWITCH_CLIENT_ID),
        'Authorization': 'OAuth {}'.format(settings.TWITCH_KEY)
    }

    r = requests.get(url, headers=headers)
    if r:
        return r.json()['data'][0]


def get_twitch_follow_time(from_id, to):
    url = 'https://api.twitch.tv/helix/users/follows?from_id={}&to_id={}'.format(from_id, to)
    headers = {
        'Client-ID': '{}'.format(settings.TWITCH_CLIENT_ID),
        'Authorization': 'OAuth {}'.format(settings.TWITCH_KEY)
    }
    r = requests.get(url, headers=headers)
    if r.json()['data']:
        return r.json()['data'][0]
