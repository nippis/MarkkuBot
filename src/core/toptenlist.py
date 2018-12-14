def toptenlist(db, chat_id, var):
    topten_unsorted = db.get_counter_top(chat_id, var, 10)

    counter = {}

    for i in topten_unsorted:
        if i["count"] != 0:
            counter[i["username"]] = i["count"]

    text = ""
    lista = ""
    number = 1

    if len(counter) == 0:
        text = "'{}'-laskuri on kaikilla tyhjä.".format(var)

    else:
        sorted_usernames = sorted(counter, key=counter.__getitem__, reverse=True)

        for user in sorted_usernames:
            lista += str(number) + ". " + user + ": " + str(counter[user]) + "\n"
            number += 1

            text = "Top {} in {}:\n{}".format(len(counter), var, lista)

    return text