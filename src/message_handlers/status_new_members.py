from core.printlog import printlog
from core.camera_versus_text import camera_versus_text

def status_new_members(bot, update):
    printlog(update, "new member")

    msg = camera_versus_text()

    update.message.reply_text(msg)