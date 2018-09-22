from core.get_ids import get_ids
#TODO collection

def count_and_write(update, var):
    user_id, chat_id = get_ids(update)

    # Älä laske blacklistattuja
    if (blacklist_collection.find_one({ "user_id": user_id }) != None):
        return

    # TODO: siirrä setOnInsertin sisälle
    # TODO: tsekkaa onko nimi Not Found, tsekkaa onko käyttäjänimi muuttunu järkeväks, jos on niin päivitä
    username = "Not found"
    if update.message.from_user.username is not None:
        username = update.message.from_user.username

    # countIncrementer kertoo $inc-operaattorille, mitä kasvatetaan ja kuinka paljon.
    # Jos kenttää ei löydy, $inc luo sen samalla numeroarvolla
    countIncrementer = {
        "count.messages": 0,
        "count.stickers": 0,
        "count.photos": 0,
        "count.gifs": 0,
        "count.commands": 0,
        "count.kiitos": 0
    }
    countIncrementer["count." + var] = 1
    
    # Update_one päivittää yhden dokumentin, eli yhden käyttäjän yhdessä chatissa.
    # Boolean lopussa on upsert-parametri, = jos queryn mätsäävää dokumenttia ei löydy, se luodaan.
    # SetOnInsert kertoo mitä muita kenttiä tehdään, jos luodaan uusi dokumentti
    chats_collection.update_one(
        { "chat_id": chat_id, "user_id": user_id },
        { 
            "$inc": countIncrementer,
            "$setOnInsert": {
                "chat_title": update.message.chat.title,
                "username": username,
            }
        },
        True
    )

    # Luo compound index (voidaan käyttää vain toisella tai molemmilla parametreilla)
    chats_collection.create_index([
        ("chat_id", ASCENDING),
        ("user_id", ASCENDING)
    ], unique=True)
