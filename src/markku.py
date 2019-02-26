# coding: utf-8

from os import environ

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (BaseFilter, CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler)

from db.database_psql import DatabasePsql

from command_handlers.command_router import CommandRouter
from message_handlers.message_router import MessageRouter
    
def handlers(updater):
    dp = updater.dispatcher

    # TODO backendin valinta conffin kautta
    # Avataan tietokanta
    db = DatabasePsql()

    # Alustetaan routerit
    cr = CommandRouter(db)
    mr = MessageRouter(db)

    # Komentojen kautta toimivat
    dp.add_handler(CommandHandler('start',          add_param(cr.route_command, "start")))
    dp.add_handler(CommandHandler('darkroom',       add_param(cr.route_command, "darkroom")))
    dp.add_handler(CommandHandler('stats',          add_param(cr.route_command, "stats")))
    dp.add_handler(CommandHandler('help',           add_param(cr.route_command, "help")))
    dp.add_handler(CommandHandler('noutaja',        add_param(cr.route_command, "noutaja")))
    dp.add_handler(CommandHandler('protip',         add_param(cr.route_command, "protip")))
    dp.add_handler(CommandHandler('kysymys',        add_param(cr.route_command, "kysymys")))
    dp.add_handler(CommandHandler('topten',         add_param(cr.route_command, "topten"), pass_args=True))

    # Blacklist
    dp.add_handler(CommandHandler('blacklist',      add_param(cr.add_blacklist, "blacklist")))
    dp.add_handler(CommandHandler('unblacklist',    add_param(cr.remove_blacklist, "unblacklist")))
    dp.add_handler(CallbackQueryHandler(cr.blacklist_confirm))

    # Suoraa viestiä urkkivat kilkkeet
    dp.add_handler(MessageHandler(Filters.sticker,                          add_param(mr.route_command, "msg_sticker")))
    dp.add_handler(MessageHandler(Filters.text,                             add_param(mr.route_command, "msg_text")))
    dp.add_handler(MessageHandler(Filters.photo,                            add_param(mr.route_command, "msg_photo")))
    dp.add_handler(MessageHandler(Filters.document,                         add_param(mr.route_command, "msg_gif")))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,   add_param(mr.route_command, "status_new_members")))

def add_param(funcToCall, paramToPass):
    def localFunction(bot, update, args=[]):
        funcToCall(bot, update, paramToPass, args)
    return localFunction

def main():
    updater = Updater(token=environ["TG_TOKEN"])
    handlers(updater)

    updater.start_polling()


main()
