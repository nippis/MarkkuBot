from core.printlog import printlog

def camera_versus(bot, update):
    printlog(update, "camera versus")

    _, chat_id = get_ids(update)
    count_and_write(update, "commands")

    msg = camera_versus_text()
    
    bot.send_message(chat_id=chat_id, text=msg)