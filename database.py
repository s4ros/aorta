import settings
import sqlite3
import sys


class AortaDatabase(object):
    def __init__(self):
        self.conn = sqlite3.connect(settings.DATABASE)
        self.c = self.conn.cursor()
        self.chatters = []

    def close(self):
        self.conn.close()

    def parse_db_chatter(self, r):
        data = {}
        data['id'] = r[0]
        data['nick'] = r[1]
        data['popularity'] = r[2]
        data['money'] = r[3]
        data['last_seen'] = r[4]
        data['time_spent'] = r[5]
        data['is_following'] = r[6]
        data['is_subscribing'] = r[7]
        return data

    def process_query(self, query):
        print(self.__name__, ':: processing database QUERY: {}'.format(query))
        return self.c.execute(query)
#
# chatters
#

    def get_chatters(self):
        chatters = []
        ret = self.c.execute('SELECT * from aorta_chatter ORDER BY id')
        for r in ret:
            data = self.parse_db_chatter(r)
            chatters.append(data)
        return chatters

    def get_chatter(self, nick):
        query = """SELECT * FROM aorta_chatter WHERE nick='{}'""".format(nick)
        try:
            ret = self.c.execute(query)
            chatter = self.parse_db_chatter(ret.fetchone())
        except:
            chatter = None
        print(":::::: get_online_chatter")
        print(chatter)
        return chatter

    def add_chatter(self, nick):
        query = """INSERT INTO aorta_chatter
             (nick, popularity, 'money', last_seen, \
             time_spent, is_following, is_subscribing) \
             VALUES ("{}", 0, 0, datetime(), \
             0, 0, 0)""".format(nick)
        self.c.execute(query)
        self.conn.commit()

#
# logs
#

    def get_logs(self):
        logs = []
        ret = self.c.execute('SELECT * from aorta_log ORDER BY id')
        for r in ret:
            logs.append(r)
        return logs

    def add_log(self, chatter, txt):
        query = """INSERT INTO aorta_log
            (nick_id, date, text) VALUES
            ({}, datetime(), "{}")""".format(int(chatter['id']), txt)
        self.c.execute(query)
        self.conn.commit()

#
# popularity
#

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

#
# money
#

    # def get_money(self, nick):

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

#
# follows
#
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

#
# subscribe
#
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

#
# time
#
    def update_last_seen(self, chatter):
        query = """UPDATE aorta_chatter SET last_seen=datetime() WHERE nick="{}"
        """.format(chatter['nick'])
        self.c.execute(query)
        self.conn.commit()

    def set_time_spent(self, time):
        pass
