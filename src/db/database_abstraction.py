# Luokan poikkeukset
class DatabaseError(Exception):
    pass

class DuplicateKeyError(DatabaseError):
    pass

# Bridge-patternin abstraktio-luokka
class DatabaseAbstraction:
    def __init__(self, imp):
        self.imp = imp  # Toteuttava luokka

    def in_blacklist(self, user_id):
        val = self.imp.in_blacklist(user_id)

        if isinstance(val, bool):
            return val
        else:
            raise TypeError

    def add_blacklist(self, user_id):
        self.imp.add_blacklist(user_id)

    def remove_blacklist(self, user_id):
        self.imp.remove_blacklist(user_id)

    def increment_counter(self, user_id, chat_id, counter, amount):
        self.imp.increment_counter(user_id, chat_id, counter, amount)

    def get_counter_user(self, user_id, chat_id, counter):
        return self.imp.get_counter_user(chat_id, user_id)

    def get_counter_top(self, chat_id, counter, top_amount):
        return self.imp.get_counter_top(chat_id, counter, top_amount)

    def word_collection_add(self, chat_id, user_id, chat_title, username, \
        word, amount):
        self.imp.word_collection_add(chat_id, user_id, chat_title, \
            username, word, amount)

    def word_collection_get_chat(self, chat_id):
        return self.imp.word_collection_get_chat(chat_id)

    def word_collection_get_chat_user(self, chat_id, user_id):
        return self.imp.word_collection_get_chat_user(chat_id, user_id)

