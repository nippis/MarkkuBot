# coding: utf-8

from os import environ

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (BaseFilter, CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler)

from core.file_read import file_read

from db.database_abstraction import DatabaseAbstraction
from db.database_minimal import DatabaseMinimal

from command_handlers.command_router import CommandRouter
from message_handlers.message_router import MessageRouter
    
def handlers(updater):
    dp = updater.dispatcher

    db_imp = DatabaseMinimal()
    db = DatabaseAbstraction(db_imp)
    cr = CommandRouter(db)
    mr = MessageRouter(db)

    # Tässä alla oleville komennoille (esim darkroom) annetaan aina bot ja updater argumenteiksi
    dp.add_handler(CommandHandler('start', cr.start))
    dp.add_handler(CommandHandler('darkroom', cr.darkroom))
    dp.add_handler(CommandHandler('stats', cr.stats))
    #dp.add_handler(CommandHandler('help', help))
    #dp.add_handler(CommandHandler('noutaja', noutaja))
    #dp.add_handler(CommandHandler('toptenmsg', topten_messages))
    #dp.add_handler(CommandHandler('toptenkiitos', topten_kiitos))
    #dp.add_handler(CommandHandler('protip', protip))
    #dp.add_handler(CommandHandler('kysymys', camera_versus))
    #dp.add_handler(CommandHandler('blacklist', blacklist))
    #dp.add_handler(CommandHandler('unblacklist', unblacklist))
    #dp.add_handler(CallbackQueryHandler(blacklist_confirm))
    dp.add_handler(MessageHandler(Filters.sticker, mr.msg_sticker))
    dp.add_handler(MessageHandler(Filters.text, mr.msg_text))
    dp.add_handler(MessageHandler(Filters.photo, mr.msg_photo))
    dp.add_handler(MessageHandler(Filters.document, mr.msg_gif))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, mr.status_new_members))

def main():
    updater = Updater(token=environ["TG_TOKEN"])
    handlers(updater)

    updater.start_polling()

#masterlist = file_read("masterlist.json")
#sticker_list = masterlist["Stickers"]
#protip_list = masterlist["Tips"]
#camera_list = masterlist["Cameras"]
#
#tg_token = environ["TG_TOKEN"]


main()
