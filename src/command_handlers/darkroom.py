import json
from urllib.request import urlopen

from core.printlog import printlog
from core.count_and_write import count_and_write

# Lukee netistä valosensorin datan ja kertoo onko kerhohuoneella valot päällä
def darkroom(bot, update):
    printlog(update, "darkroom")

    _, chat_id = get_ids(update)
    count_and_write(update, "commands")
    
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