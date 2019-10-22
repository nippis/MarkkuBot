import sys
from os import environ  
from collections import Counter
import psycopg2

class DatabasePsql:
    def __init__(self):
        self.counters = [
            "messages",
            "kiitos",
            "stickers",
            "photos",
            "gifs",
            "commands",
        ]

    def open_connection(self):
        db_name = environ["POSTGRES_DB"]
        db_user = environ["POSTGRES_USER"]
        db_pass = environ["POSTGRES_PASSWORD"]
        db_host = "db"
        self.table_name = "name"
        self.table_counter = "counter"
        self.table_word = "word"
        self.table_blacklist = "blacklist"

        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
        )

        # TODO: testaa onko legit yhteys

        return conn

    def get_counters(self):
        return self.counters


    def in_blacklist(self, user_id):

        conn = self.open_connection()

        sql =   "SELECT 1 " \
                "FROM {} " \
                "WHERE user_id = {};"

        conn.cursor.execute(sql.format(self.table_blacklist, user_id))

        return conn.cursor.fetchone() is not None


    def update_name(self, id, name):
        conn = self.open_connection()

        sql =   "INSERT INTO {0} (id, name) " \
                "VALUES ({1}, '{2}') " \
                "ON CONFLICT (id) DO UPDATE " \
                "SET name = '{2}';"        

        conn.cursor.execute(sql.format(self.table_name, id, name))

        conn.conn.commit()


    def add_blacklist(self, user_id):
        sql =   "INSERT INTO {0} " \
                "VALUES ({4});" \
                " " \
                "DELETE FROM {1} " \
                "WHERE id={4}; " \
                "DELETE FROM {2} " \
                "WHERE user_id={4}; " \
                "DELETE FROM {3} " \
                "WHERE user_id={4}; " \
        
        self.cursor.execute(sql.format(self.table_blacklist, self.table_name, self.table_counter, self.table_word, user_id))

        self.conn.commit()


    def remove_blacklist(self, user_id):
        sql =   "DELETE from {} " \
                "WHERE user_id = {};"

        self.cursor.execute(sql.format(self.table_blacklist, user_id))
        self.conn.commit()


    def increment_counter(self, user_id, chat_id, counter, amount):
        # inkrementoidaan, jossei riviä ole, lisätään se

        sql =   "INSERT INTO {0} (user_id, chat_id, {1}) " \
                "VALUES ({2}, {3}, {4}) " \
                "ON CONFLICT (user_id, chat_id) DO UPDATE " \
                "SET {1} = {0}.{1} + {4};"

        self.cursor.execute(sql.format(self.table_counter, counter, user_id, chat_id, amount))
        self.conn.commit()


    def get_counter_user(self, user_id, chat_id, counter):
        # palauttaa käyttäjä, chätti parin laskurin

        sql =   "SELECT {} " \
                "FROM {} " \
                "WHERE user_id = {} AND chat_id = {};"

        self.cursor.execute(sql.format(counter, self.table_counter, user_id, chat_id))
        
        return self.cursor.fetchone()[0]


    def get_counter_top(self, chat_id, counter, top_amount):
        # nimitaulusta nimet, countterista laskurin arvo
        # kursori antaa ne tupleina -> muutetaan dictiin ja palautetaan

        sql =   "SELECT {0}.{2}, {1}.name " \
                "FROM {0} " \
                "INNER JOIN {1} " \
                "ON {0}.user_id = {1}.id " \
                "WHERE {0}.chat_id={3} " \
                "AND {0}.{2}!=0 " \
                "ORDER BY {0}.{2} DESC " \
                "LIMIT {4};"

        self.cursor.execute(sql.format(self.table_counter, self.table_name, counter, chat_id, top_amount))

        res = self.cursor.fetchall()

        return dict((y, x) for x, y in res)

        
    def word_collection_add(self, user_id, chat_id, word, amount):
        # user, chat, sana yhdistelmät uniikkeja
        # jos ei löydy -> lisätään, jos löytyy, lisätään amount counttiin

        sql =   "INSERT INTO {0} (user_id, chat_id, word, count) " \
                "VALUES ({1}, {2}, '{3}', {4}) " \
                "ON CONFLICT (user_id, chat_id, word) DO UPDATE " \
                "SET count = {0}.count + {4}; "

        self.cursor.execute(sql.format(self.table_word, user_id, chat_id, word, amount))
        self.conn.commit()


    def word_collection_get_chat(self, chat_id):
        # TODO tätä ei käytetä vielä missään, en tiedä miten pitäisi tehdä

        sql = "select * from word where chat_id = {};"
        self.cursor.execute(sql.format(chat_id))

        return self.cursor.fetchall()


    def word_collection_get_chat_user(self, chat_id, user_id):
        pass

if __name__ == "__main__":
    asd = DatabasePsql()
