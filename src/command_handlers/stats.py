from core.printlog import printlog
from core.count_and_write import count_and_write
from core.get_ids import get_ids
#TODO collection

def stats(bot, update):
    printlog(update, "stats")

    user_id, chat_id = get_ids(update)
    # Älä poista tai muuta paikkaa ellet korjaa samalla, miten Markku käsittelee käyttäjän jota ei ole blacklistattu,
    # mutta jolla ei ole vielä mitään statseja
    count_and_write(update, "commands")

    user = chats_collection.find_one({ "chat_id": chat_id, "user_id": user_id })

    if (user == None):
        update.message.reply_text("Markku ei seuraa sinua. Käytä komentoa /unblacklist , jos haluat seurannan käyttöön.\n" \
                                  "Markku does not track you. Use the command /unblacklist to enable tracking.")

    user_data = user["count"]

    sticker_percent = "?"
    kiitos_percent = "?"

    if user_data["stickers"] + user_data["messages"] != 0:
        sticker_percent = round(((user_data["stickers"]) / (user_data["stickers"] + user_data["messages"]) * 100), 2)

    if user_data["messages"] != 0:
        kiitos_percent = round(((user_data["kiitos"]) / (user_data["messages"]) * 100), 2)

    msg = "@{}:\nMessages: {}".format(user["username"], user_data["messages"])
    msg += "\nStickers: {} ({}%)".format(user_data["stickers"], sticker_percent)
    msg += "\nKiitos: {} ({}%)".format(user_data["kiitos"], kiitos_percent)
    msg += "\nPhotos: {}".format(user_data["photos"])

    bot.send_message(chat_id=chat_id, text=msg)