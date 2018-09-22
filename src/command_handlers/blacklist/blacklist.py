def blacklist(bot, update):
    printlog(update, "blacklist")

    user_id, _ = get_ids(update)

    if (update.message.chat.type != "private"):
        update.message.reply_text("Ole hyvä ja lähetä tämä pyyntö yksityisviestillä.\n" \
                                  "Please send this request via private message.")
        return
    
    if (blacklist_collection.find_one({ "user_id": user_id }) != None):
        update.message.reply_text("Tietosi on jo poistettu, eikä sinua seurata.\n" \
                                  "Your information is already deleted and you are not tracked.")
        return
    
    keyboard = [[InlineKeyboardButton("Ei (No)", callback_data="false"),
                 InlineKeyboardButton("Kyllä (Yes)", callback_data="true")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Haluatko, että kaikki henkilöivät tietosi poistetaan Markun tietokannasta," \
                              "ja käyttäjäsi lisätään \"älä seuraa\"-listalle?\n\n" \
                              "Do you want to delete all of your personifiable information from Markku's database" \
                              "and add your user to the \"do not track\" list?",
                              reply_markup=reply_markup)