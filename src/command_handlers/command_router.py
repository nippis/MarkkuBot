# -*- coding: utf-8 -*-
import json
from urllib.request import urlopen, Request
from urllib.error import URLError

from core.printlog import printlog
from core.count_and_write import count_and_write
from core.get_ids import get_ids

class CommandRouter():
    def __init__(self, db):
        self.db = db

    def start(self, bot, update):
        printlog(update, "start")

        _, chat_id = get_ids(update) # Ignoraa user_id, tätä käytetään paljon
        count_and_write(self.db, update, "commands")

        bot.send_message(chat_id=chat_id, text="Woof woof")

    def stats(self, bot, update):
        printlog(update, "stats")

        user_id, chat_id = get_ids(update)

        count_and_write(self.db, update, "commands")

        if self.db.in_blacklist(user_id):
            update.message.reply_text("Markku ei seuraa sinua. Käytä komentoa /unblacklist , jos haluat seurannan käyttöön.\n" \
                                    "Markku does not track you. Use the command /unblacklist to enable tracking.")
            return

        count_messages = self.db.get_counter_user(user_id, chat_id, "count.messages")
        count_stickers = self.db.get_counter_user(user_id, chat_id, "count.stickers")
        count_kiitos = self.db.get_counter_user(user_id, chat_id, "count.kiitos")
        count_photos = self.db.get_counter_user(user_id, chat_id, "count.photos")

        sticker_percent = 0
        kiitos_percent = 0

        if count_stickers + count_messages != 0:
            sticker_percent = round((count_stickers / (count_stickers+count_messages) * 100), 2)
        
        if count_messages != 0:
            kiitos_percent = round((count_kiitos / count_messages * 100), 2)

        msg = "@{}:\nMessages: {}".format(update.message.from_user.username, count_messages)
        msg += "\nStickers: {} ({}%)".format(count_stickers, sticker_percent)
        msg += "\nKiitos: {} ({}%)".format(count_kiitos, kiitos_percent)
        msg += "\nPhotos: {}".format(count_photos)        

        bot.send_message(chat_id=chat_id, text=msg)

    # Lukee netistä valosensorin datan ja kertoo onko kerhohuoneella valot päällä
    def darkroom(self, bot, update):
        printlog(update, "darkroom")

        _, chat_id = get_ids(update)
        count_and_write(self.db, update, "commands")
        
        try:
            with urlopen("https://ttkamerat.fi/darkroom/api/v1/sensors/latest") as url:
                sensor_data = json.loads(url.read().decode())

                value_light = 0
                isDarkroomPopulated = False

                # JSON härössä muodossa, sen takia teemme näin. Esimerkki:
                #   {"entries": [{"value": 191, "sensor": "light1", "inserted": "2018-07-27T16:18:43.589Z"}]}
                for sensor in sensor_data["entries"]:
                    if sensor["sensor"] == "light1":
                        value_light = sensor["value"]

                if value_light > 100:
                    isDarkroomPopulated = True

                if isDarkroomPopulated:
                    reply = "Joku on pimiöllä :O\n"
                else:
                    reply = "Pimiö tyhjä :(\n"

                bot.send_message(chat_id=chat_id, text=reply)
        except URLError as e:
            print(e.reason)
            bot.send_message(chat_id=chat_id, text="Ei ny onnistunu (%s)" % e.reason)

    def help(self, bot, update):
        printlog(update, "help")

        _, chat_id = get_ids(update)
        count_and_write(self.db, update, "commands")

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
                "Botin koodit: @eltsu7, @kulmajaba ja @anttimoi\n" \
                "Valosensorit ja siihen koodit: @anttimoi"

        bot.send_message(chat_id=chat_id, text=reply)            

    def noutaja(self, bot, update):
        printlog(update, "noutaja")

        _, chat_id = get_ids(update)
        count_and_write(self.db, update, "commands")

        url = "https://dog.ceo/api/breed/retriever/golden/images/random"

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        with urlopen(req) as page:
            retriever_data = json.loads(page.read().decode())

            picture_link = retriever_data["message"]

            bot.sendPhoto(chat_id=chat_id, photo=picture_link)