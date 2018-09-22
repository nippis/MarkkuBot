from core.printlog import printlog
from core.count_and_write import count_and_write

def help(bot, update):
    printlog(update, "help")

    _, chat_id = get_ids(update)
    count_and_write(update, "commands")

    reply = "Komennot:\n" \
            "/darkroom - Kertoo onko joku pimiöllä\n" \
            "/stats - Chattikohtaiset statsit\n" \
            "/toptenmsg - Chatin kovimmat viestittelijät\n"\
            "/toptenkiitos - Chatin kovimmat kiitostelijat\n"\
            "/noutaja - Postaa satunnaisen noutajakuvan\n"\
            "/protip - Antaa ammatti valo kuvaus vinkin!\n"\
            "/blacklist - Poista omat tietosi Markun tietokannasta ja estä uusien tallentaminen, lähetä privana Markulle\n"\
            "/unblacklist - Salli omien tietojesi tallentaminen blacklist-komennon jälkeen, lähetä privana Markulle\n"\
            "\n" \
            "Botin koodit: @eltsu7 ja @kulmajaba\n" \
            "Valosensorit ja siihen koodit: @anttimoi"

    bot.send_message(chat_id=chat_id, text=reply)