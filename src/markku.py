# coding: utf-8

from os import environ

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (BaseFilter, CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler)

from db.database_mongo import DatabaseMongo

from command_handlers.command_router import CommandRouter
from message_handlers.message_router import MessageRouter
    
def handlers(updater):
    dp = updater.dispatcher

    # TODO backendin valinta conffin kautta
    # Avataan tietokanta
    db = DatabaseMongo()

    # Alustetaan routerit
    cr = CommandRouter(db)
    mr = MessageRouter(db)

    # Komentojen kautta toimivat
    dp.add_handler(CommandHandler('start', cr.start))
    dp.add_handler(CommandHandler('darkroom', cr.darkroom))
    dp.add_handler(CommandHandler('stats', cr.stats))
    dp.add_handler(CommandHandler('help', cr.help))
    dp.add_handler(CommandHandler('noutaja', cr.noutaja))
    dp.add_handler(CommandHandler('topten', cr.topten, pass_args=True))
    dp.add_handler(CommandHandler('protip', cr.protip))
    dp.add_handler(CommandHandler('kysymys', cr.camera_versus))

    # Blacklist
    dp.add_handler(CommandHandler('blacklist', cr.add_blacklist))
    dp.add_handler(CommandHandler('unblacklist', cr.remove_blacklist))
    dp.add_handler(CallbackQueryHandler(cr.blacklist_confirm))

    # Suoraa viestiä urkkivat kilkkeet
    dp.add_handler(MessageHandler(Filters.sticker, mr.msg_sticker))
    dp.add_handler(MessageHandler(Filters.text, mr.msg_text))
    dp.add_handler(MessageHandler(Filters.photo, mr.msg_photo))
    dp.add_handler(MessageHandler(Filters.document, mr.msg_gif))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, mr.status_new_members))

def main():
    updater = Updater(token=environ["TG_TOKEN"])
    handlers(updater)

    updater.start_polling()


main()
