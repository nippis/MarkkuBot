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
        # TODO mitä jos rivii ei oo?

        sql = "update {0} set {1} = {1} + {2} where user_id = {3} and chat_id = {4};"
        self.cursor.execute(sql.format(self.table_counter, counter, amount, user_id, chat_id))
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
        sql = "insert into {} where user_id = {} and chat_id = {} values"

    def word_collection_get_chat(self, chat_id):
        pass

    def word_collection_get_chat_user(self, chat_id, user_id):
        pass

if __name__ == "__main__":
    asd = DatabasePsql()

    asd.get_counter_top(-1001162147452, "messages", 10)
