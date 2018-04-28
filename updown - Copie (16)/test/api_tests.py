"""
Created on 26.01.2013
Modified on 05.02.2017
@author: ivan sanchez
@author: mika oja
"""
import unittest, copy
import json

import flask

import updown.resources as resources
import updown.database as database

DB_PATH = "db/updown_test.db"
ENGINE = database.Engine(DB_PATH)

MASONJSON = "application/vnd.mason+json"
JSON = "application/json"
HAL = "application/hal+json"
FORUM_USER_PROFILE ="/profiles/user-profile/"
FORUM_MESSAGE_PROFILE = "/profiles/currency-profile/"

#Tell Flask that I am running it in testing mode.
resources.app.config["TESTING"] = True
#Necessary for correct translation in url_for
resources.app.config["SERVER_NAME"] = "localhost:5000"

#Database Engine utilized in our testing
resources.app.config.update({"Engine": ENGINE})

#Other database parameters.
initial_currencies = 20
initial_users = 5


class ResourcesAPITestCase(unittest.TestCase):
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        """ Creates the database structure. Removes first any preexisting
            database file
        """
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        """Remove the testing database"""
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        """
        Populates the database
        """
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Activate app_context for using url_for
        self.app_context = resources.app.app_context()
        self.app_context.push()
        #Create a test client
        self.client = resources.app.test_client()

    def tearDown(self):
        """
        Remove all records from database
        """
        ENGINE.clear()
        self.app_context.pop()

class CurrenciesTestCase (ResourcesAPITestCase):

    #Anonymous user
    currency_1_request = {       
        "currencycode": "DDD",
        "currencyname": "TTT"
    }    

    url = "/updown/api/currencies/"

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Currencies)

    def test_add_currency(self):
        """
        Test adding currency to the database.
        """
        print("("+self.test_add_currency.__name__+")", self.test_add_currency.__doc__)

        resp = self.client.post(resources.api.url_for(resources.Currencies),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.currency_1_request)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)

    def test_add_currency_wrong_media(self):
        """
        Test adding currency with a media different than json
        """
        print("("+self.test_add_currency_wrong_media.__name__+")", self.test_add_currency_wrong_media.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Currencies),
                                headers={"Content-Type": "text"},
                                data=self.currency_1_request.__str__()
                               )
        self.assertTrue(resp.status_code == 415)

class CurrencyTestCase (ResourcesAPITestCase):

    currency_req_1 = {
        "currencycode": "FFF",
        "currencyname": "ZZZ"
    }
    currency_wrong_req_1 = {
        "dagadah": "dandou"
    }
	
    def setUp(self):
        super(CurrencyTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Currency,
                                         currencyid="1",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.Currency,
                                               currencyid="19",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        _url = "/updown/api/currency/2"
        print("("+self.test_url.__name__+")", self.test_url.__doc__)
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Currency)

    def test_wrong_url(self):
        """
        Checks that GET Currency return correct status code if given a
        wrong message
        """
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_modify_currency(self):
        """
        Modify an exsiting currency and check that the currency has been modified correctly in the server
        """
        print("("+self.test_modify_currency.__name__+")", self.test_modify_currency.__doc__)
        resp = self.client.put(self.url,
                               data=json.dumps(self.currency_req_1),
                               headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 204)

        #Check that the currency has been modified
        resp2 = self.client.get(self.url)
        self.assertEqual(resp2.status_code, 200)

        data = json.loads(resp2.data.decode("utf-8"))
        #Check that the currency has been modified with the new data
        self.assertEqual(data["currencycode"], self.currency_req_1["currencycode"])
        self.assertEqual(data["currencyname"], self.currency_req_1["currencyname"])

    def test_modify_unexisting_currency(self):
        """
        Try to modify a currency that does not exist
        """
        print("("+self.test_modify_unexisting_currency.__name__+")", self.test_modify_unexisting_currency.__doc__)
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.currency_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 404)

    def test_modify_wrong_currency(self):
        """
        Try to modify a currency sending wrong data
        """
        print("("+self.test_modify_wrong_currency.__name__+")", self.test_modify_wrong_currency.__doc__)
        resp = self.client.put(self.url,
                               data=json.dumps(self.currency_wrong_req_1),
                               headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 400)

    def test_delete_currency(self):
        """
        Checks that Delete Currency return correct status code if corrected delete
        """
        print("("+self.test_delete_currency.__name__+")", self.test_delete_currency.__doc__)
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 204)
        resp2 = self.client.get(self.url)
        self.assertEqual(resp2.status_code, 404)

    def test_delete_unexisting_currency(self):
        """
        Checks that Delete Currency return correct status code if given a wrong address
        """
        print("("+self.test_delete_unexisting_currency.__name__+")", self.test_delete_unexisting_currency.__doc__)
        resp = self.client.delete(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

class UsersTestCase (ResourcesAPITestCase):

    #Anonymous user
    user_1_request = {       
        "username": "uuu",
		"fullname": "fff",
        "password": "ppp"
    }    

    url = "/updown/api/users/"

    def setUp(self):
        super(UsersTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Users,
                                         _external=False)

	
    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Users)

class UserTestCase (ResourcesAPITestCase):

    currency_req_1 = {
        "currencycode": "FFF",
        "currencyname": "ZZZ"
    }
    currency_wrong_req_1 = {
        "dagadah": "dandou"
    }
	
    def setUp(self):
        super(UserTestCase, self).setUp()
        self.url = resources.api.url_for(resources.User,
                                         username="nadiro",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.User,
                                               username="dandan",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        _url = "/updown/api/user/nadiro"
        print("("+self.test_url.__name__+")", self.test_url.__doc__)
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.User)

    def test_wrong_url(self):
        """
        Checks that GET Currency return correct status code if given a
        wrong message
        """
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)


class ChoicesTestCase (ResourcesAPITestCase):

    currency_req_1 = {
        "currencycode": "FFF",
        "currencyname": "ZZZ"
    }
    currency_wrong_req_1 = {
        "dagadah": "dandou"
    }
	
    def setUp(self):
        super(ChoicesTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Choices,
                                         username="nadiro",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.Choices,
                                               username="dandan",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        _url = "/updown/api/choices/nadiro"
        print("("+self.test_url.__name__+")", self.test_url.__doc__)
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Choices)

class ExchangesTestCase (ResourcesAPITestCase):

    #Anonymous user
    currency_1_request = {       
        "currencycode": "DDD",
        "currencyname": "TTT"
    }    

    url = "/updown/api/exchanges/"

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Exchanges)


		
if __name__ == "__main__":
    print("Start running tests")
    unittest.main()
