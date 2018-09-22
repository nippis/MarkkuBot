from core.printlog import printlog
from core.count_and_write import count_and_write

def msg_sticker(bot, update):
    printlog(update, "sticker")

    count_and_write(update, "stickers")