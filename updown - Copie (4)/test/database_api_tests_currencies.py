'''
Created on 13.02.2014
Modified on 25.02.2018
Database interface testing for all currencies related methods.
The user has a data model represented by the following User dictionary:
    {'currency_id':1, currency_code: 'USD','currency__name': 'United state dollar'}
    }
    where:
     - currency_id: a uniq if for te currency
     - currency_code: the currency code.
     - currency__name: the full name of the currency.

@author: ivan
'''
import sqlite3, unittest
from updown import database

#Path to the database file, different from the deployment db
DB_PATH = 'db/updown_test.db'
ENGINE = database.Engine(DB_PATH)

#CONSTANTS DEFINING DIFFERENT CURRENCY AND CURRENCY PROPERTIES
NEW_CURRENCY_CODE='XXX'
NEW_CURRENCY_NAME='NEW ANONYMOUS CURRENCY'
NEW_CURRENCY_DICTIONARY={'currency_code':NEW_CURRENCY_CODE,'currency_name':NEW_CURRENCY_NAME}

EXISTING_CURRENCY_CODE='EURO'
EXISTING_CURRENCY_NAME='EURO'

MODIFY_CURRENCY_ID=2
MODIFY_CURRENCY_CODE='DZD'
MODIFY_CURRENCY_NAME='Algerian Dinard'

MODIFY_CURRENCY_ID_NOT_FOUND=80

GET_CURRENCY_ID=4
GET_CURRENCY_CODE='GBP'
GET_CURRENCY_NAME='Pound sterling'

GET_CURRENCY_NOT_FOUND=80

DELETE_CURRENCY_ID=4
DELETE_CURRENCY_ID_NOT_FOUND=80

class CurrencyDBAPITestCase(unittest.TestCase):

    '''
    Test cases for the Users related methods.
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

    def test_create_currency(self):
        '''
        Test create new currency success
        ''' 
        print('('+self.test_create_currency.__name__+')', \
              self.test_create_currency.__doc__)
        currency_id = self.connection.create_currency(NEW_CURRENCY_CODE,NEW_CURRENCY_NAME)  
        self.assertIsNotNone(currency_id)
        #Check that the currency has been really added
        resp2=self.connection.get_curreny(currency_id)
        self.assertEqual(NEW_CURRENCY_DICTIONARY['currency_code'], resp2['currency_code'])
        self.assertEqual(NEW_CURRENCY_DICTIONARY['currency_name'], resp2['currency_name'])

    def test_create_existing_currency(self):
        '''
        Test create existing currency success
        ''' 
        print('('+self.test_create_existing_currency.__name__+')', \
              self.test_create_existing_currency.__doc__)
        currency_id = self.connection.create_currency(EXISTING_CURRENCY_CODE,EXISTING_CURRENCY_NAME)
        #Check that the currency has not been really added
        self.assertIsNone(currency_id)
				
    def test_modify_currency(self):
        '''
        Test update of currency success
        ''' 
        print('('+self.test_modify_currency.__name__+')', \
              self.test_modify_currency.__doc__)
        currency_id = self.connection.modify_currency(MODIFY_CURRENCY_ID, MODIFY_CURRENCY_CODE, MODIFY_CURRENCY_NAME)
        self.assertIsNotNone(currency_id)
        #Check that the currency has been really updated
        resp2=self.connection.get_curreny(currency_id)
        self.assertEqual(MODIFY_CURRENCY_CODE, resp2['currency_code'])
        self.assertEqual(MODIFY_CURRENCY_NAME, resp2['currency_name'])
		
    def test_modify_none_exsting_currency(self):
        '''
        Test update of currency failure
        ''' 
        print('('+self.test_modify_none_exsting_currency.__name__+')', \
              self.test_modify_none_exsting_currency.__doc__)
        currency_id = self.connection.modify_currency(MODIFY_CURRENCY_ID_NOT_FOUND, MODIFY_CURRENCY_CODE, MODIFY_CURRENCY_NAME)
        #Check that the currency has not been really updated
        self.assertIsNone(currency_id)		
		
		
    def test_get_currency(self):
        '''
        Test getting values of currency
        ''' 
        print('('+self.test_get_currency.__name__+')', \
              self.test_get_currency.__doc__)
        resp = self.connection.get_curreny(GET_CURRENCY_ID)
        #Check that the currency is retrieved
        self.assertEqual(GET_CURRENCY_CODE, resp['currency_code'])
        self.assertEqual(GET_CURRENCY_NAME, resp['currency_name'])
		
    def test_get_currency_not_found(self):
        '''
        Test getting values of currency not found
        ''' 
        print('('+self.test_get_currency_not_found.__name__+')', \
              self.test_get_currency_not_found.__doc__)
        currency_id = self.connection.get_curreny(GET_CURRENCY_NOT_FOUND)
        #Check that the currency is ot retrieved
        self.assertIsNone(currency_id)			

    def test_delete_currency(self):
        '''
        Test deletion of currency success
        ''' 
        print('('+self.test_delete_currency.__name__+')', \
              self.test_delete_currency.__doc__)
        resp = self.connection.delete_currency(DELETE_CURRENCY_ID)
        self.assertTrue(resp)
		
    def test_delete_currency_not_found(self):
        '''
        Test deletion of currency failure
        ''' 
        print('('+self.test_delete_currency_not_found.__name__+')', \
              self.test_delete_currency_not_found.__doc__)
        resp = self.connection.delete_currency(DELETE_CURRENCY_ID_NOT_FOUND)
        self.assertEqual(resp,False)		
  
		
if __name__ == '__main__':
    print('Start running message tests')
    unittest.main()
