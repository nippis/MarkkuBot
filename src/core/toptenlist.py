def toptenlist(db, chat_id, var):
    topten_unsorted = db.get_counter_top(chat_id, var, 10)

    counter = {}

    for i in topten_unsorted:
        counter[i["username"]] = i["count"]

    text = ""
    number = 1

    sorted_usernames = sorted(counter, key=counter.__getitem__, reverse=True)

    for user in sorted_usernames:
        text += str(number) + ". " + user + ": " + str(counter[user]) + "\n"
        number += 1

    return text, number - 1