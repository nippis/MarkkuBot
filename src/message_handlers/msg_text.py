import random

from core.printlog import printlog
from core.count_and_write import count_and_write
from core.parse_and_count import parse_and_count

def msg_text(bot, update):
    printlog(update, "text")

    _, chat_id = get_ids(update)
    count_and_write(update, "messages")

    message = update.message.text.lower()

    parse_and_count(update)

    lotto = random.randint(1, 201)

    if "kiitos" in message:
        count_and_write(update, "kiitos")

        if lotto < 11:
            update.message.reply_text("Kiitos")
        elif lotto < 16:
            sticker_index = random.randint(0, len(sticker_list) - 1)
            bot.send_sticker(chat_id=chat_id, sticker=sticker_list[sticker_index])

        elif lotto < 17:
            update.message.reply_text("Ole hyvä")

    elif "markku" in message and "istu" in message:
        if lotto < 91:
            bot.send_message(chat_id=chat_id, text="*istuu*")
        else:
            bot.send_message(chat_id=chat_id, text="*paskoo lattialle*")

    elif "huono markku" in message:
        bot.send_message(chat_id=chat_id, text="w00F")

    elif "markku perkele" in message:
        bot.send_message(chat_id=chat_id, text="woof?")

    elif "filmi" in message and lotto < 11:
        bot.send_message(chat_id=chat_id, text="Filmi best")