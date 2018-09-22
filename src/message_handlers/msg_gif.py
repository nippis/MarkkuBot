from core.printlog import printlog
from core.count_and_write import count_and_write

def msg_gif(bot, update):
    printlog(update, "gif")

    count_and_write(update, "gifs")