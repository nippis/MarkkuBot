from urllib.request import Request, urlopen

from core.printlog import printlog
from core.count_and_write import count_and_write

#TODO masterlist

def noutaja(bot, update):
    printlog(update, "noutaja")

    _, chat_id = get_ids(update)
    count_and_write(update, "commands")

    url = "https://dog.ceo/api/breed/retriever/golden/images/random"

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    with urlopen(req) as page:
        retriever_data = json.loads(page.read().decode())

        picture_link = retriever_data["message"]

        bot.sendPhoto(chat_id=chat_id, photo=picture_link)