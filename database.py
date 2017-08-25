import settings
import sqlite3


class AortaDatabase(object):
    def __init__(self):
        self.conn = sqlite3.connect(settings.DATABASE)
        self.c = self.conn.cursor()
        self.chatters = []

    def get_chatters(self):
        chatters = []
        ret = self.c.execute('SELECT * from aorta_chatter ORDER BY id')
        for r in ret:
            data = {}
            data['nick'] = r[1]
            data['id'] = r[0]
            data['is_following'] = r[5]
            data['is_subscribing'] = r[6]
            chatters.append(data)
        return chatters

    def get_logs(self):
        logs = []
        ret = self.c.execute('SELECT * from aorta_log ORDER BY id')
        for r in ret:
            logs.append(r)
        return logs

    def add_chatter(self, nick):
        query = """INSERT INTO aorta_chatter
                             (nick, popularity, money, last_seen, \
                             time_spent, is_following, is_subscribing) \
                             VALUES ("{}", 0, 0, datetime(), \
                             0, 0, 0)""".format(nick)
        self.c.execute(query)
        self.conn.commit()

    def add_log(self, chatter, txt):
        query = """INSERT INTO aorta_log
            (nick_id, date, text) VALUES
            ({}, datetime(), "{}")""".format(int(chatter['id']), txt)
        self.c.execute(query)
        self.conn.commit()

    def inc_popularity(self, chatter):
        query = """UPDATE aorta_chatter SET popularity=popularity+1 WHERE nick="{}"
        """.format(chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def dec_popularity(self, chatter):
        query = """UPDATE aorta_chatter SET popularity=popularity-1 WHERE nick="{}"
        """.format(chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def add_money(self, chatter, amount):
        query = """UPDATE aorta_chatter SET money=money+{} WHERE nick="{}"
        """.format(amount, chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def remove_money(self, chatter, amount):
        query = """UPDATE aorta_chatter SET money=money-{} WHERE nick="{}"
        """.format(amount, chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def set_follow(self, chatter):
        query = """UPDATE aorta_chatter SET is_following=1 WHERE nick="{}"
        """.format(chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def unset_follow(self, chatter):
        query = """UPDATE aorta_chatter SET is_following=0 WHERE nick="{}"
        """.format(chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def set_sub(self, chatter):
        query = """UPDATE aorta_chatter SET is_subscribing=1 WHERE nick="{}"
        """.format(chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def unset_sub(self, chatter):
        query = """UPDATE aorta_chatter SET is_subscribing=0 WHERE nick="{}"
        """.format(chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def update_last_seen(self, chatter):
        query = """UPDATE aorta_chatter SET last_seen=datetime() WHERE nick="{}"
        """.format(chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def set_time_spent(self, time):
        pass
