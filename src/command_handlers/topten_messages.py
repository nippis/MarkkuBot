from core.toptenlist import toptenlist
from core.printlog import printlog
from core.count_and_write import count_and_write

def topten_messages(bot, update):
    printlog(update, "toptenmessages")

    _, chat_id = get_ids(update)
    count_and_write(update, "commands")

    list, number = toptenlist(chat_id, "messages")

    text = "Top " + str(number) + " viestittelijät:\n" + list

    bot.send_message(chat_id=chat_id, text=text)