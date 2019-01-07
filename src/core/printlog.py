def printlog(update, msg_type):
    username = update.message.from_user.username
    content = ""

    print("Type: ", msg_type, "\nUsername: ", username)

    if msg_type == "sticker":
        content = update.message.sticker.file_id
    elif msg_type == "text":
        content = update.message.text

    if content != "":
        print("Content: ", content)

    print()