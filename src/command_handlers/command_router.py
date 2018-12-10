# -*- coding: utf-8 -*-
import json
from urllib.request import urlopen, Request
from urllib.error import URLError
import random

from core.printlog import printlog
from core.count_and_write import count_and_write
from core.get_ids import get_ids
from core.toptenlist import toptenlist
from core.camera_versus_text import camera_versus_text

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import masterlist

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

        count_messages = self.db.get_counter_user(user_id, chat_id, "messages")
        count_stickers = self.db.get_counter_user(user_id, chat_id, "stickers")
        count_kiitos = self.db.get_counter_user(user_id, chat_id, "kiitos")
        count_photos = self.db.get_counter_user(user_id, chat_id, "photos")

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

    def topten_kiitos(self, bot, update): #TODO username
        printlog(update, "toptenkiitos")

        _, chat_id = get_ids(update)
        count_and_write(self.db, update, "commands")

        list, number = toptenlist(self.db, chat_id, "count.kiitos")

        text = "Top " + str(number) + " kiitostelijat:\n" + list

        bot.send_message(chat_id=chat_id, text=text)

    def topten_messages(self, bot, update):
        printlog(update, "toptenmessages")

        _, chat_id = get_ids(update)
        count_and_write(self.db, update, "commands")

        list, number = toptenlist(self.db, chat_id, "count.messages")

        text = "Top " + str(number) + " viestittelijät:\n" + list

        bot.send_message(chat_id=chat_id, text=text)

    def protip(self, bot, update):
        printlog(update, "protip")

        _, chat_id = get_ids(update)
        count_and_write(self.db, update, "commands")

        protip_list = masterlist.tips

        protip_index = random.randint(0, len(protip_list) - 1)

        bot.send_message(chat_id=chat_id, text=protip_list[protip_index])

    def camera_versus(self, bot, update):
        printlog(update, "camera versus")

        _, chat_id = get_ids(update)
        count_and_write(self.db, update, "commands")

        msg = camera_versus_text()
        bot.send_message(chat_id=chat_id, text=msg)

    def add_blacklist(self, bot, update):
        printlog(update, "blacklist")

        user_id, _ = get_ids(update)

        if (update.message.chat.type != "private"):
            update.message.reply_text("Ole hyvä ja lähetä tämä pyyntö yksityisviestillä.\n" \
                                    "Please send this request via private message.")
            return

        
        if self.db.in_blacklist(user_id):
            print("1")
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

        print("3")

    def remove_blacklist(self, bot, update):
        user_id, _ = get_ids(update)

        if (update.message.chat.type != "private"):
            update.message.reply_text("Ole hyvä ja lähetä tämä pyyntö yksityisviestillä\n" \
                                    "Please send this request via private message")
            return

        if self.db.in_blacklist(user_id):
            
            self.db.remove_blacklist(user_id)
            update.message.reply_text("Markku seuraa sinua taas.\n" \
                                    "Markku is tracking you again.\n\n" \
                                    "*sniff sniff* Woof!")
        else:
            update.message.reply_text("Et ole Markun \"älä seuraa\"-listalla.\n" \
                                    "You are not on Markku's \"do not track\" list.")

    def blacklist_confirm(self, bot, update):
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
        self.db.add_blacklist(user_id)
