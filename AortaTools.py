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
