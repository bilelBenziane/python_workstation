'''
Created on 13.02.2014
Modified on 26.02.2018
Database interface testing for all exchange related methods.

@author: ivan
'''
import sqlite3, unittest
from updown import database

#Path to the database file, different from the deployment db
DB_PATH = 'db/updown_test.db'
ENGINE = database.Engine(DB_PATH)

#CONSTANTS DEFINING DIFFERENT EXCHANGE RATES
FROM_CURRENCY=1
TO_CURRENCY=2
EXACT_DATE=20180219
EXCHAGE_RATE=1.5

ADD_ERROR_FROM_CURRENCY=1
ADD_ERROR_TO_CURRENCY=3
ADD_ERROR_EXACT_DATE=20180219
ADD_ERROR_EXCHAGE_RATE=1.5

GET_EXCHANGE_NONE_CURRENCY_FROM=1
GET_EXCHANGE_NONE_CURRENCY_TO=2
GET_EXCHANGE_NONE_DATE_FROM=2
GET_EXCHANGE_NONE_DATE_TO=2

GET_EXCHANGE_CURRENCY_FROM=2
GET_EXCHANGE_CURRENCY_TO=4
GET_EXCHANGE_DATE_FROM=20180219
GET_EXCHANGE_DATE_TO=20180222
GET_EXCHANGE_DATE=20180220
GET_EXCHANGE_RATE=1.5

class ExchangeDBAPITestCase(unittest.TestCase):

    '''
    Test cases for the Exchange related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        #This method load the initial values from updown_data_dump.sql
        ENGINE.populate_tables()
        #Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()

    def test_add_exchange_user_success(self):
        '''
        Test create new user success
        ''' 
        print('('+self.test_add_exchange_user_success.__name__+')', \
              self.test_add_exchange_user_success.__doc__)
        resp = self.connection.add_exchange(FROM_CURRENCY,TO_CURRENCY,EXACT_DATE,EXCHAGE_RATE)  
        self.assertIsNotNone(resp)
		
    def test_add_exchange_user_failure(self):
        '''
        Test create new user failure
        ''' 
        print('('+self.test_add_exchange_user_failure.__name__+')', \
              self.test_add_exchange_user_failure.__doc__)
        resp = self.connection.add_exchange(ADD_ERROR_FROM_CURRENCY,ADD_ERROR_TO_CURRENCY,ADD_ERROR_EXACT_DATE,ADD_ERROR_EXCHAGE_RATE)  
        self.assertIsNone(resp)

    def test_get_exchange_none(self):
        '''
        Test get exchange nothing found
        ''' 
        print('('+self.test_get_exchange_none.__name__+')', \
              self.test_get_exchange_none.__doc__)
        resp = self.connection.get_exchange(GET_EXCHANGE_NONE_CURRENCY_FROM,GET_EXCHANGE_NONE_CURRENCY_TO,GET_EXCHANGE_NONE_DATE_FROM,GET_EXCHANGE_NONE_DATE_TO)  
        self.assertEqual(resp,[])
		
    def test_get_exchange(self):
        '''
        Test get exchange found
        ''' 
        print('('+self.test_get_exchange.__name__+')', \
              self.test_get_exchange.__doc__)
        rates = self.connection.get_exchange(GET_EXCHANGE_CURRENCY_FROM,GET_EXCHANGE_CURRENCY_TO,GET_EXCHANGE_DATE_FROM,GET_EXCHANGE_DATE_TO)  
        for rate in rates:
            if rate['exact_date'] == GET_EXCHANGE_DATE:
                self.assertEqual(rate['from_currency'],GET_EXCHANGE_CURRENCY_FROM)
                self.assertEqual(rate['to_currency'],GET_EXCHANGE_CURRENCY_TO)
                self.assertEqual(rate['exchange_rate'],GET_EXCHANGE_RATE)
                self.assertEqual(rate['exact_date'],GET_EXCHANGE_DATE)
                print(rate)

		
if __name__ == '__main__':
    print('Start running exchange tests')
    unittest.main()
