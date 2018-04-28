import sqlite3, unittest
from forum import database

DB_PATH = 'db/updown_test.db'
ENGINE = database.Engine(DB_PATH)
CURRENCY1_ID = 'msg-1'

class MessageDBAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        try:
          #This method load the initial values from forum_data_dump.sql
          ENGINE.populate_tables()
          #Creates a Connection instance to use the API
          self.connection = ENGINE.connect()
        except Exception as e: 
        #For instance if there is an error while populating the tables
          ENGINE.clear()

    def tearDown(self):
        self.connection.close()
        ENGINE.clear()

    def test_delete_currency(self):
        print('('+self.test_delete_currency.__name__+')', \
              self.test_delete_currency.__doc__)
        resp = self.connection.delete_currency(CURRENCY1_ID)
        self.assertTrue(resp)

if __name__ == '__main__':
    print('Start running message tests')
    unittest.main()
