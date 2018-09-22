class DatabaseMongo:
    def in_blacklist(self):
        return True

    def add_blacklist(self, user_id):
        pass

    def remove_blacklist(self, user_id):
        pass

    def increment_counter(self, user_id, chat_id, counter, amount):
        pass

    def get_counter_top(self, chat_id, counter, top_amount):
        return "jtn"

    def word_collection_add(self, chat_id, user_id, chat_title, username, \
        word, amount):
        pass

    def word_collection_get_chat(self, chat_id):
        return "jtn2"

    def word_collection_get_chat_user(self, chat_id, user_id):
        return "jtn"

