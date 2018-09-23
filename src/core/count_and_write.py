# -*- coding: utf-8 -*-

from core.get_ids import get_ids
#TODO collection

def count_and_write(db, update, var):
    print("count_and_write", var)
    user_id, chat_id = get_ids(update)

    # Älä laske blacklistattuja
    if db.in_blacklist(user_id):
        return

    db.increment_counter(user_id, chat_id, "count."+var, 1)
