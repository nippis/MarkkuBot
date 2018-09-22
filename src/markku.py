# coding: utf-8

import logging
import random
import re
from collections import Counter
from os import environ
from urllib.request import Request, urlopen

from pymongo import ASCENDING, MongoClient
from pymongo import errors as MongoErrors
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (BaseFilter, CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler)

from core.printlog import printlog
from core.file_read import file_read
from core.get_ids import get_ids
from core.count_and_write import count_and_write

from command_handlers.camera_versus import camera_versus
from command_handlers.darkroom import darkroom 
from command_handlers.help import help
from command_handlers.noutaja import noutaja
from command_handlers.protip import protip
from command_handlers.start import start
from command_handlers.stats import stats
from command_handlers.topten_kiitos import topten_kiitos
from command_handlers.topten_messages import topten_messages

from command_handlers.blacklist.blacklist import blacklist
from command_handlers.blacklist.unblacklist import unblacklist
from command_handlers.blacklist.blacklist_confirm import blacklist_confirm

from message_handlers.msg_gif import msg_gif
from message_handlers.msg_photo import msg_photo
from message_handlers.msg_sticker import msg_sticker
from message_handlers.msg_text import msg_text
from message_handlers.status_new_members import status_new_members
    
def handlers(updater):
    dp = updater.dispatcher

    # Tässä alla oleville komennoille (esim darkroom) annetaan aina bot ja updater argumenteiksi
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('darkroom', darkroom))
    dp.add_handler(CommandHandler('stats', stats))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('noutaja', noutaja))
    dp.add_handler(CommandHandler('toptenmsg', topten_messages))
    dp.add_handler(CommandHandler('toptenkiitos', topten_kiitos))
    dp.add_handler(CommandHandler('protip', protip))
    dp.add_handler(CommandHandler('kysymys', camera_versus))
    dp.add_handler(CommandHandler('blacklist', blacklist))
    dp.add_handler(CommandHandler('unblacklist', unblacklist))
    dp.add_handler(CallbackQueryHandler(blacklist_confirm))
    dp.add_handler(MessageHandler(Filters.sticker, msg_sticker))
    dp.add_handler(MessageHandler(Filters.text, msg_text))
    dp.add_handler(MessageHandler(Filters.photo, msg_photo))
    dp.add_handler(MessageHandler(Filters.document, msg_gif))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, status_new_members))

def main():
    updater = Updater(token=tg_token)
    handlers(updater)

    updater.start_polling()

masterlist = file_read("masterlist.json")
sticker_list = masterlist["Stickers"]
protip_list = masterlist["Tips"]
camera_list = masterlist["Cameras"]

tg_token = environ["TG_TOKEN"]
db_name = environ["DB_NAME"]
chats_coll_name = environ["CHATS_COLL_NAME"]
words_coll_name = environ["WORDS_COLL_NAME"]
blacklist_coll_name = environ["BLACKLIST_COLL_NAME"]

# TODO: failaa jos ei saada yhteyttä
db_client = MongoClient("mongodb://mongo:27017", serverSelectionTimeoutMS=1000)
db = db_client[db_name]
chats_collection = db[chats_coll_name]
words_collection = db[words_coll_name]
blacklist_collection = db[blacklist_coll_name]

main()
