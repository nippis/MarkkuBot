import sys
from os import environ  
from collections import Counter
import psycopg2

class DatabasePsql:
    def __init__(self):
        db_name = environ["PSQL_DBNAME"]
        db_user = environ["PSQL_USER"]
        db_pass = environ["PSQL_PASS"]
        db_host = environ["PSQL_HOST"]
        db_port = environ["PSQL_PORT"]
        self.table_name =       environ["PSQL_TABLE_NAME"]
        self.table_counter =    environ["PSQL_TABLE_COUNTER"]
        self.table_word =       environ["PSQL_TABLE_WORD"]
        self.table_blacklist =  environ["PSQL_TABLE_BLACKLIST"]

        self.conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            port=db_port
        )

        self.conn = psycopg2.connect("dbname=eltsu7 user=eltsu7")


        self.cursor = self.conn.cursor()


        self.counters = [
            "messages",
            "kiitos",
            "stickers",
            "photos",
            "gifs",
            "commands",
        ]

    def get_counters(self):
        return self.counters

    def in_blacklist(self, user_id):
        sql = "select 1 from {} where user_id = {};"
        self.cursor.execute(sql.format(self.table_blacklist, user_id))

        return self.cursor.fetchone() is not None

    def add_blacklist(self, user_id):
        sql = "insert into {} values ({});"
        self.cursor.execute(sql.format(self.table_blacklist, user_id))
        self.conn.commit()

    def remove_blacklist(self, user_id):
        sql = "delete from {} where user_id = {};"
        self.cursor.execute(sql.format(self.table_blacklist, user_id))
        self.conn.commit()

    def increment_counter(self, user_id, chat_id, counter, amount):
        sql =   "insert into {0} (user_id, chat_id, {1}) values ({2}, {3}, {4})" \
                "on conflict do update set {1} += EXCLUDED.{1}"

        self.cursor.execute(sql.format(self.table_counter, counter, user_id, chat_id, amount))
        self.conn.commit()

    def get_counter_user(self, user_id, chat_id, counter):
        sql = "select {} from {} where user_id = {} and chat_id = {};"
        self.cursor.execute(sql.format(counter, self.table_counter, user_id, chat_id))
        
        return self.cursor.fetchone()[0]

    def get_counter_top(self, chat_id, counter, top_amount):
        # TODO tämän voi tehdä jollain join hommalla??

        sql = "select user_id, {0} from {1} where chat_id = {2} order by {0} desc limit {3};"
        self.cursor.execute(sql.format(counter, self.table_counter, chat_id, top_amount))

        counter_top = {}

        results = self.cursor.fetchall()

        for res in results:
            self.cursor.execute("select name from {} where id = {}".format(self.table_name, res[0]))

            username = self.cursor.fetchone()[0]

            counter_top[username] = res[1]

        return counter_top

        
    def word_collection_add(self, user_id, chat_id, word, amount):
        sql =   "insert into {0} values ({1}, {2}, {3}, {4})" \
                "on conflict do update set {4} += EXCLUDED.{4}"

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
