def unblacklist(bot, update):
    user_id, _ = get_ids(update)

    if (update.message.chat.type != "private"):
        update.message.reply_text("Ole hyvä ja lähetä tämä pyyntö yksityisviestillä\n" \
                                  "Please send this request via private message")
        return

    deleteResult = blacklist_collection.delete_one(
        { "user_id": user_id }
    )

    if (deleteResult.deleted_count != 0):
        update.message.reply_text("Markku seuraa sinua taas.\n" \
                                  "Markku is tracking you again.\n\n" \
                                  "*sniff sniff* Woof!")
    else:
        update.message.reply_text("Et ole Markun \"älä seuraa\"-listalla.\n" \
                                  "You are not on Markku's \"do not track\" list.")