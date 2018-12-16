import sys
from os import environ  
from pymongo import ASCENDING, MongoClient
from pymongo import errors as MongoErrors
from collections import Counter

class DatabaseMongo:
    def __init__(self):
        db_name = environ["DB_NAME"]
        chats_coll_name = environ["CHATS_COLL_NAME"]
        words_coll_name = environ["WORDS_COLL_NAME"]
        blacklist_coll_name = environ["BLACKLIST_COLL_NAME"]

        
        # lisäargumentilla 'local' db:n osoite vaihtuu localhostiin testauksen helpottamiseksi
        if len(sys.argv) == 2 and sys.argv[1] == 'local':
            db_address = "localhost:27017"
        else:
            db_address = "mongodb://mongo:27017"
            
        self.db_client = MongoClient(db_address, serverSelectionTimeoutMS=1000)
        db = self.db_client[db_name]

        self.db_client.server_info()

        self.chats_collection = db[chats_coll_name]
        self.words_collection = db[words_coll_name]
        self.blacklist_collection = db[blacklist_coll_name]

        self.counters = [
            "messages",
            "stickers",
            "photos",
            "gifs",
            "commands",
            "kiitos"
        ]

    def get_counters(self):
        return self.counters

    def in_blacklist(self, user_id):
        cur = self.blacklist_collection.find({ "user_id": user_id })

        return (cur.count() != 0)

    def add_blacklist(self, user_id):
        self.blacklist_collection.insert_one({"user_id": user_id})

        self.chats_collection.delete_many(
            { "user_id": user_id }
        )
        self.words_collection.delete_many(
            { "user_id": user_id }
        )
        
        self.blacklist_collection.create_index([("user_id", ASCENDING)], unique=True)

    def remove_blacklist(self, user_id):
        self.blacklist_collection.delete_one({ "user_id": user_id })

    def increment_counter(self, user_id, chat_id, var, amount, chat_title, username):
        countIncrementer = {
            "count.messages": 0,
            "count.stickers": 0,
            "count.photos": 0,
            "count.gifs": 0,
            "count.commands": 0,
            "count.kiitos": 0
        }
        countIncrementer["count." + var] = 1
        
        # Update_one päivittää yhden dokumentin, eli yhden käyttäjän yhdessä chatissa.
        # Boolean lopussa on upsert-parametri, = jos queryn mätsäävää dokumenttia ei löydy, se luodaan.
        # SetOnInsert kertoo mitä muita kenttiä tehdään, jos luodaan uusi dokumentti
        self.chats_collection.update_one(
            { "chat_id": chat_id, "user_id": user_id },
            { "$inc": countIncrementer },
            True
        )
        self.chats_collection.update_one(
            { "chat_id": chat_id, "user_id": user_id },
            { "$set": { "username" : username, "chat_title" : chat_title }}
        )

    def get_counter_user(self, user_id, chat_id, counter):
        return self.chats_collection.find({ "chat_id": chat_id, "user_id": user_id })[0]["count"][counter]

    def get_counter_top(self, chat_id, var, top_amount):
        cursor = self.chats_collection.aggregate([
            { "$match": { "chat_id": chat_id }},
            { "$project": { "_id": 0, "username": 1, "count": "$count." + var }},
            { "$sort": { "count": -1 }},
            { "$limit": top_amount }
        ])

        return cursor
        
    def word_collection_add(self, user_id, chat_id, chat_title, username, \
        word, amount):
            
        self.words_collection.update_one(
            { "chat_id": chat_id, "user_id": user_id },
            { "$inc": {word: amount}},
            True
        )

        self.chats_collection.update_one(
            { "chat_id": chat_id, "user_id": user_id },
            { "$set": { "username" : username, "chat_title" : chat_title }}
        )

    def word_collection_get_chat(self, chat_id):
        return "jtn2"

    def word_collection_get_chat_user(self, chat_id, user_id):
        return "jtn"

