# -*- coding: utf-8 -*-
import operator

class DatabaseMinimal:
    def __init__(self):
        self.blacklist = set()
        self.counters = dict()
        self.word_counter = dict()

    def in_blacklist(self, user_id):
        return user_id in self.blacklist

    def add_blacklist(self, user_id):
        # TODO poista data
        self.blacklist.add(user_id)

    def remove_blacklist(self, user_id):
        try:
            self.blacklist.remove(user_id)
        except KeyError:
            pass # Ei ollut alunperinkään blacklistissä

    def increment_counter(self, user_id, chat_id, counter, amount):
        if counter not in self.counters:
            self.counters[counter] = dict()
            self.counters[counter][chat_id] = dict()

        if chat_id not in self.counters[counter]:
            self.counters[counter][chat_id] = dict()

        if user_id not in self.counters[counter][chat_id]:
            self.counters[counter][chat_id][user_id] = amount
        else:
            self.counters[counter][chat_id][user_id] += amount

    def get_counter_user(self, user_id, chat_id, counter):
        try:
            return self.counters[counter][chat_id][user_id]
        except KeyError:
            return 0

    def get_counter_top(self, chat_id, counter, top_amount):
        try:
            chat_counter = self.counters[counter][chat_id]
            sorted_counter = sorted(chat_counter.items(), key=operator.itemgetter(1))
            sorted_counter_return = []

            for item in sorted_counter:
                sorted_counter_return.append({'username': item[0], 'count': item[1]})

            return sorted_counter_return[:top_amount]
        except KeyError:
            pass

    def word_collection_add(self, chat_id, user_id, chat_title, username, \
        word, amount):
        if chat_id in self.word_counter:
            if user_id in self.word_counter[chat_id]:
                if word in self.word_counter[chat_id][user_id]:
                    self.word_counter[chat_id][user_id][word] += amount
                else:
                    self.word_counter[chat_id][user_id][word] = amount
            else:
                self.word_counter[chat_id][user_id] = dict()
                self.word_counter[chat_id][user_id][word] = amount
        else:
            self.word_counter[chat_id] = dict()
            self.word_counter[chat_id][user_id] = dict()
            self.word_counter[chat_id][user_id][word] = amount

    def word_collection_get_chat(self, chat_id):
        try:
            word_collection = self.word_counter[chat_id]
            words_return = dict()

            for user, words in word_collection.items():
                for word, amount in words.items():
                    if word in words_return:
                        words_return[word] += amount
                    else:
                        words_return[word] = amount

            return words_return
        except KeyError:
            return 0        

    def word_collection_get_chat_user(self, chat_id, user_id):
        try:
            return self.word_counter[chat_id][user_id]
        except KeyError:
            return 0

