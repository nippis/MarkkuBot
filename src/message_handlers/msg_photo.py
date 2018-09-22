from core.printlog import printlog
from core.count_and_write import count_and_write

def msg_photo(bot, update):
    printlog(update, "photo")

    count_and_write(update, "photos")