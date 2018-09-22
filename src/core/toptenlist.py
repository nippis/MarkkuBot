def toptenlist(chat_id, var):
    topten_sorted = db.get_counter_top(chat_id, var, 10)

    text = ""
    number = 1

    for user in topten_sorted:
        text += str(number) + ". " + user["username"] + ": " + str(user["count"]) + "\n"
        number += 1

    return text, len(topten_sorted)