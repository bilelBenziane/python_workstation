'''
Created on 13.02.2014
Modified on 25.02.2018
Database interface testing for all users related methods.

@author: ivan
'''
import sqlite3, unittest
from updown import database

#Path to the database file, different from the deployment db
DB_PATH = 'db/updown_test.db'
ENGINE = database.Engine(DB_PATH)

#CONSTANTS DEFINING DIFFERENT USERS AND USERS PROPERTIES
CREATE_USER_NAME='Dandou'
CREATE_USER_FULL_NAME='Dandou full name'
CREATE_USER_PASSWORD='Dandou pass'

MODIFY_USER_NAME='nadiro'
MODIFY_USER_FULL_NAME='Dandou full name'
MODIFY_USER_PASSWORD='Dandou pass'

NON_EXISTIN_USERNAME='fake'
NON_EXISTIN_FULLNAME='fake fullname'
NON_EXISTIN_PASSWORD='fake password'

DELETE_USERNAME='nadiro'
DELETE_USERNAME_FAKE='nadirzzzzz'

USER_CHOICE_USERNAME='nadiro'
USER_CHOICE_FROM_CURRENCY=1
USER_CHOICE_TO_CURRENCY=2
USER_CHOICE_DATE_FROM=20180204
USER_CHOICE_DATE_TO=20180214

DELETE_USER_CHOICE_USERNAME='nadiro'
DELETE_USER_CHOICE_FROM_CURRENCY=1
DELETE_USER_CHOICE_TO_CURRENCY=3
DELETE_USER_CHOICE_DATE_FROM=20180220
DELETE_USER_CHOICE_DATE_TO=20180222

USER_USERNAME_FAKE='fake'
USER_CHOICE_USERNAME_FAKE='fake'
class UserDBAPITestCase(unittest.TestCase):

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

    def test_create_user(self):
        '''
        Test create new user success
        ''' 
        print('('+self.test_create_user.__name__+')', \
              self.test_create_user.__doc__)
        user_name = self.connection.create_user(CREATE_USER_FULL_NAME,CREATE_USER_NAME,CREATE_USER_PASSWORD)  
        self.assertIsNotNone(user_name)
        #Check that the user has been really added
        resp2=self.connection.get_user(user_name)
        self.assertEqual(CREATE_USER_FULL_NAME, resp2['fullname'])
        self.assertEqual(CREATE_USER_PASSWORD, resp2['password'])
		
    def test_modify_user_success(self):
        '''
        Test modify user success
        ''' 
        print('('+self.test_modify_user_success.__name__+')', \
              self.test_modify_user_success.__doc__)
        #Check that the user has been really modified
        user_name=self.connection.modify_user(MODIFY_USER_NAME,MODIFY_USER_FULL_NAME,MODIFY_USER_PASSWORD)
        self.assertEqual(MODIFY_USER_NAME, user_name)
		
    def test_modify_user_failure(self):
        '''
        Test modify user failure
        ''' 
        print('('+self.test_modify_user_failure.__name__+')', \
              self.test_modify_user_failure.__doc__)
        #Check that the user has not been really modified
        user_name=self.connection.modify_user(NON_EXISTIN_USERNAME,NON_EXISTIN_FULLNAME,NON_EXISTIN_PASSWORD)
        self.assertIsNone(user_name)
		
    def test_delete_user_success(self):
        '''
        Test delete user success
        ''' 
        print('('+self.test_delete_user_success.__name__+')', \
              self.test_delete_user_success.__doc__)
        #Check that the user has been really deleted
        resp=self.connection.delete_user(DELETE_USERNAME)
        self.assertTrue(resp)

    def test_delete_user_failure(self):
        '''
        Test delete user failure
        ''' 
        print('('+self.test_delete_user_failure.__name__+')', \
              self.test_delete_user_failure.__doc__)
        #Check that the user has npt been really deleted
        resp=self.connection.delete_user(DELETE_USERNAME_FAKE)
        self.assertFalse(resp)
		
    def test_add_user_choice(self):
        '''
        Test add user choice
        ''' 
        print('('+self.test_add_user_choice.__name__+')', \
              self.test_add_user_choice.__doc__)
        #Check that the user has choice been really deleted
        resp=self.connection.add_user_choice(USER_CHOICE_USERNAME,USER_CHOICE_FROM_CURRENCY,USER_CHOICE_TO_CURRENCY,USER_CHOICE_DATE_FROM,USER_CHOICE_DATE_TO)
        self.assertIsNotNone(resp)     

    def test_add_user_choice_failure(self):
        '''
        Test add user choice
        ''' 
        print('('+self.test_add_user_choice_failure.__name__+')', \
              self.test_add_user_choice_failure.__doc__)
        #Check that the user has choice been really deleted
        resp=self.connection.add_user_choice(USER_CHOICE_USERNAME_FAKE,USER_CHOICE_FROM_CURRENCY,USER_CHOICE_TO_CURRENCY,USER_CHOICE_DATE_FROM,USER_CHOICE_DATE_TO)
        self.assertIsNone(resp)     
		
    def test_delete_user_choice(self):
        '''
        Test delete user choice
        ''' 
        print('('+self.test_delete_user_choice.__name__+')', \
              self.test_delete_user_choice.__doc__)
        #Check that the user choice has  been really deleted
        resp=self.connection.delete_user_choice(DELETE_USER_CHOICE_USERNAME,DELETE_USER_CHOICE_FROM_CURRENCY,DELETE_USER_CHOICE_TO_CURRENCY,DELETE_USER_CHOICE_DATE_FROM,DELETE_USER_CHOICE_DATE_TO)
        self.assertTrue(resp)     
        
		
if __name__ == '__main__':
    print('Start running message tests')
    unittest.main()
