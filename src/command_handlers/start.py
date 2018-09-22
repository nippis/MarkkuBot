# -*- coding: utf-8 -*-

from core.printlog import printlog
from core.count_and_write import count_and_write
from core.get_ids import get_ids

def start(bot, update):
    printlog(update, "start")

    _, chat_id = get_ids(update) # Ignoraa user_id, tätä käytetään paljon
    count_and_write(update, "commands")

    bot.send_message(chat_id=chat_id, text="Woof woof")