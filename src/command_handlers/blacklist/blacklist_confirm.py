def blacklist_confirm(bot, update):
    query = update.callback_query

    username = query.from_user.username
    user_id = query.from_user.id

    print("Type: blacklist_confirm", "\nUsername: ", username)

    if (query.data == "false"):
        bot.edit_message_text(text="Käyttäjätietojen poistaminen peruttu.\n" \
                                   "The deletion of user information has been cancelled.",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return
    
    bot.edit_message_text(text="Käyttäjätiedot poistettu, ja käyttäjää ei seurata jatkossa.\n" \
                                "User information deleted, and the user will not be tracked.",
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)

    # Poista kaikki käyttäjän dokumentit
    chats_collection.delete_many(
        { "user_id": user_id }
    )
    words_collection.delete_many(
        { "user_id": user_id }
    )

    try:
        blacklist_collection.insert_one({
            "user_id": user_id
        })
        blacklist_collection.create_index([
            ("user_id", ASCENDING)
        ], unique=True)
    except MongoErrors.DuplicateKeyError:
        print("User {} already blacklisted".format(username))