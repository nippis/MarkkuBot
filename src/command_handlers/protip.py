import random

from core.printlog import printlog
from core.count_and_write import count_and_write
from core.get_ids import get_ids

#TODO masterlist

def protip(bot, update):
    printlog(update, "protip")

    _, chat_id = get_ids(update)
    count_and_write(update, "commands")

    protip_index = random.randint(0, len(protip_list) - 1)

    bot.send_message(chat_id=chat_id, text=protip_list[protip_index])