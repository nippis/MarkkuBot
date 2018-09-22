#TODO collection

def toptenlist(chat_id, var):
    cursor = chats_collection.aggregate([
        { "$match": { "chat_id": chat_id }},
        { "$project": { "_id": 0, "username": 1, "count": "$count." + var }},
        { "$sort": { "count": -1 }},
        { "$limit": 10 }
    ])

    topten_sorted = list(cursor)

    text = ""
    number = 1

    for user in topten_sorted:
        text += str(number) + ". " + user["username"] + ": " + str(user["count"]) + "\n"
        number += 1

    return text, len(topten_sorted)