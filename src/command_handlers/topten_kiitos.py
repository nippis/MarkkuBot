from core.toptenlist import toptenlist
from core.printlog import printlog
from core.count_and_write import count_and_write

def topten_kiitos(bot, update):
    printlog(update, "toptenkiitos")

    _, chat_id = get_ids(update)
    count_and_write(update, "commands")

    list, number = toptenlist(chat_id, "kiitos")

    text = "Top " + str(number) + " kiitostelijat:\n" + list

    bot.send_message(chat_id=chat_id, text=text)