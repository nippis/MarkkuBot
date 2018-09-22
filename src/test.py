# -*- coding: utf-8 -*-
from StringIO import StringIO
import unittest

from test.dummy_bot import DummyBot
from test.dummy_update import DummyUpdate
from test.dummy_message import DummyMessage
from test.dummy_chat import DummyChat
from test.dummy_user import DummyUser

from core.get_ids import get_ids

from db.database_abstraction import DatabaseAbstraction
from db.database_minimal import DatabaseMinimal

from command_handlers.start import start

update_generic = DummyUpdate(chat=DummyChat('609'), from_user=DummyUser('1377', 'kurkkumopo'))

class TestGetIds(unittest.TestCase):
    def test_equals(self):
        update = DummyUpdate(chat=DummyChat('609'), from_user=DummyUser('1377', 'kurkkumopo'))
        self.assertEqual(get_ids(update), ('1377', '609'))

@unittest.skip("Tietokanta ei vielä käytössä")
class TestStart(unittest.TestCase):
    def test_equals(self):
        out = StringIO()
        bot = DummyBot(out=out)
        start(bot, update_generic)
        botText = out.getvalue().strip()
        self.assertEqual(botText, "Woof woof")

if __name__ == '__main__':
    print("Yksikkötestit")

    db_min = DatabaseMinimal()
    dba = DatabaseAbstraction(db_min)

    print('Tieto kanta', dba.in_blacklist())

    unittest.main()