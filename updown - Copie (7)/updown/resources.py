# coding= utf-8
'''
Created on 26.01.2013
Modified on 02.03.2018
@author: mika oja
@author: ivan
'''

import json

from urllib.parse import unquote
from flask import Flask, request, Response, g, _request_ctx_stack, redirect, send_from_directory
from flask_restful import Resource, Api, abort
from werkzeug.exceptions import NotFound,  UnsupportedMediaType

from updown import database

#Constants for hypermedia formats and profiles
MASON = "application/vnd.mason+json"
JSON = "application/json"
FORUM_USER_PROFILE = "/profiles/user-profile/"
FORUM_MESSAGE_PROFILE = "/profiles/message-profile/"

UPDOWN_CURRENCY_PROFILE = "/profiles/currency-profile/"

ERROR_PROFILE = "/profiles/error-profile"

ATOM_THREAD_PROFILE = "https://tools.ietf.org/html/rfc4685"

# Fill these in

#STUDENT APIARY PROJECT SHOULD HAVE THE STUDENTS PROJECT URL"
#STUDENT_APIARY_PROJECT = "https://pwpforum.docs.apiary.io"
STUDENT_APIARY_PROJECT = "https://pwp2018exercise320.docs.apiary.io"
APIARY_PROFILES_URL = STUDENT_APIARY_PROJECT+"/#reference/profiles/"
APIARY_RELS_URL = STUDENT_APIARY_PROJECT+"/#reference/link-relations/"

USER_SCHEMA_URL = "/forum/schema/user/"
LINK_RELATIONS_URL = "/updown/link-relations/"


#Define the application and the api
app = Flask(__name__, static_folder="static", static_url_path="/.")
app.debug = True
# Set the database Engine. In order to modify the database file (e.g. for
# testing) provide the database path   app.config to modify the
#database to be used (for instance for testing)
app.config.update({"Engine": database.Engine()})
#Start the RESTful API.
api = Api(app)

# These two classes below are how we make producing the resource representation
# JSON documents manageable and resilient to errors. As noted, our mediatype is
# Mason. Similar solutions can easily be implemented for other mediatypes.


class MasonObject(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)        
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs

class UpdownObject(MasonObject):    
    """
    A convenience subclass of MasonObject that defines a bunch of shorthand 
    methods for inserting application specific objects into the document. This
    class is particularly useful for adding control objects that are largely
    context independent, and defining them in the resource methods would add a 
    lot of noise to our code - not to mention making inconsistencies much more
    likely!

    In the forum code this object should always be used for root document as 
    well as any items in a collection type resource. 
    """

    def __init__(self, **kwargs):
        """
        Calls dictionary init method with any received keyword arguments. Adds
        the controls key afterwards because hypermedia without controls is not 
        hypermedia. 
        """

        super(UpdownObject, self).__init__(**kwargs)
        self["@controls"] = {}

    def add_control_users_all(self):
        """
        This adds the users-all link to an object. Intended for the document object.  
        """

        self["@controls"]["forum:users-all"] = {
            "href": api.url_for(Users),
            "title": "List users"
        }

    def add_control_add_currency(self):
        """
        This adds the add-currency control to an object. Intended for the  
        document object. Here you can see that adding the control is a bunch of 
        lines where all we're basically doing is nested dictionaries to 
        achieve the correctly formed JSON document representation. 
        """

        self["@controls"]["updown:add-currency"] = {
            "href": api.url_for(Currencies),
            "title": "Create currency",
            "encoding": "json",
            "method": "POST",
            "schema": self._currency_schema()
        }

    def add_control_delete_currency(self, id):
        """
        Adds the delete control to an object. This is intended for any 
        object that represents a currency.

        : param str id: currency id 
        """

        self["@controls"]["updown:delete"] = {
            "href": api.url_for(Currency, currencyid=id),  
            "title": "Delete this currency",
            "method": "DELETE"
        }

    def add_control_edit_currency(self, id):
        """
        Adds a the edit control to a currency object. For the schema we need
        the one that's intended for editing (it has editor instead of author).

        : param str id: currency id 
        """

        self["@controls"]["edit"] = {
            "href": api.url_for(Currency, currencyid=id),
            "title": "Edit this currency",
            "encoding": "json",
            "method": "PUT",
            "schema": {
                       "type": "object",
                       "properties": {},
                       "required": self._currency_schema()
            }
        }
		
    def _currency_schema(self):
        schema = {
            "type": "object",
            "properties": {},
            "required": ["currencycode", "currencyname"]
        }

        props = schema["properties"]
        props["currencycode"] = {
            "title": "currency_code",
            "description": "Currency code",
            "type": "string"
        }
        props["currencyname"] = {
            "title": "currency_name",
            "description": "Currency name",
            "type": "string"
        }        
        return schema

#ERROR HANDLERS

def create_error_response(status_code, title, message=None):
    """ 
    Creates a: py: class:`flask.Response` instance when sending back an
    HTTP error response

    : param integer status_code: The HTTP status code of the response
    : param str title: A short description of the problem
    : param message: A long description of the problem
    : rtype:: py: class:`flask.Response`
    """

    resource_url = None
    #We need to access the context in order to access the request.path
    ctx = _request_ctx_stack.top
    if ctx is not None:
        resource_url = request.path
    envelope = MasonObject(resource_url=resource_url)
    envelope.add_error(title, message)

    return Response(json.dumps(envelope), status_code, mimetype=MASON+";"+ERROR_PROFILE)

@app.errorhandler(404)
def resource_not_found(error):
    return create_error_response(404, "Resource not found",
                                 "This resource url does not exit")

@app.errorhandler(400)
def resource_not_found(error):
    return create_error_response(400, "Malformed input format",
                                 "The format of the input is incorrect")

@app.errorhandler(500)
def unknown_error(error):
    return create_error_response(500, "Error",
                    "The system has failed. Please, contact the administrator")

@app.before_request
def connect_db():
    """
    Creates a database connection before the request is proccessed.

    The connection is stored in the application context variable flask.g .
    Hence it is accessible from the request object.
    """

    g.con = app.config["Engine"].connect()

#HOOKS
@app.teardown_request
def close_connection(exc):
    """ 
    Closes the database connection
    Check if the connection is created. It migth be exception appear before
    the connection is created.
    """

    if hasattr(g, "con"):
        g.con.close()


#Define the resources
class Currencies(Resource):
    """
    Resource Currencies implementation
    """
    def get(self):
        """
        Get all currencies.

        INPUT parameters:
          None

        RESPONSE ENTITY BODY:
        * Media type: Mason
          https://github.com/JornWildt/Mason
         * Profile: Forum_Message
          /profiles/message_profile

        NOTE:
         * The attribute articleBody is obtained from the column messages.body
         * The attribute headline is obtained from the column messages.title
         * The attribute author is obtained from the column messages.sender
        """
        #Extract messages from database
        currencies_db = g.con.get_all_currencies()

        envelope = UpdownObject()
        envelope.add_namespace("updown", LINK_RELATIONS_URL)

        envelope.add_control("self", href=api.url_for(Currencies))
        items = envelope["items"] = []
		
        print(currencies_db)
		
        for currency in currencies_db:             
            item = UpdownObject(
                 id=currency['curency_id'],
                 code=currency['currency_code']
                )
            currency_id=currency["curency_id"]
            item.add_control("self", href=api.url_for(Currencies, id=currency['curency_id']))
            items.append(item)

        '''
        MASON = "application/vnd.mason+json"
        JSON = "application/json"
        FORUM_USER_PROFILE = "/profiles/user-profile/"
        FORUM_MESSAGE_PROFILE = "/profiles/message-profile/"
        ERROR_PROFILE = "/profiles/error-profile"
		'''			

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";"+UPDOWN_CURRENCY_PROFILE)

class Currency(Resource):
    """
    Resource Currency implementation
    """
    def get(self, currencyid):
        """
        Get the id, the code and the name of a specific curency.

        Returns status code 404 if the messageid does not exist in the database.

        INPUT PARAMETER
       : param str currencyid: The id of the currency to be retrieved from the
            system

        RESPONSE ENTITY BODY:
         * Media type: application/vnd.mason+json:
             https://github.com/JornWildt/Mason
         * Profile: Currency_Message
           /profiles/currency-profile

            Link relations used: self, text,text and text

            Semantic descriptors used: curencyid, currencycode and currencyname

        RESPONSE STATUS CODE
         * Return status code 200 if everything OK.
         * Return status code 404 if the currency was not found in the database.

        NOTE:
         * The attribute currencyid is obtained from the column currencies.currency_id
         * The attribute currencycode is obtained from the column currencies.currency_code
         * The attribute currencyname is obtained from the column currencies.curency_name
        """

        #PEFORM OPERATIONS INITIAL CHECKS
        #Get the currency from db
        currency_db = g.con.get_curreny(currencyid)
        if not currency_db:
            return create_error_response(404, "Currency not found",
                                         "There is no a currency with id %s" % currencyid)

        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = UpdownObject(
            currencyid=currency_db["currency_id"],
            currencycode=currency_db["currency_code"],
            currencyname=currency_db["currency_name"]            
        )

        envelope.add_namespace("updown", LINK_RELATIONS_URL)
		
        envelope.add_control_add_currency()
        envelope.add_control_delete_currency(currencyid)
        envelope.add_control_edit_currency(currencyid)
        envelope.add_control("profile", href=UPDOWN_CURRENCY_PROFILE)        
        envelope.add_control("collection", href=api.url_for(Currencies))
        envelope.add_control("self", href=api.url_for(Currency, currencyid=currencyid))                
							 
	
        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";"+UPDOWN_CURRENCY_PROFILE)
		
    def delete(self, currencyid):
        """
        Deletes a currency from the Updown API.

        INPUT PARAMETERS:
       : param str currencyid: The id of the currency to be deleted

        RESPONSE STATUS CODE
         * Returns 204 if the currency was deleted
         * Returns 404 if the currency was not deleted or does not exist.
        """

        #PERFORM DELETE OPERATIONS
        if g.con.delete_currency(currencyid):
            return "", 204
        else:
            #Send error message
            return create_error_response(404, "Unknown currency",
                                         "There is no a curency with id %s" % currencyid
                                        )

    def put(self, currencyid):
        """
        Modifies the code and and name of this currency.

        INPUT PARAMETERS:
       : param str currencyid: The id of the crrency to be modified

        REQUEST ENTITY BODY:
        * Media type: JSON
        * Profile: Updown_Profile
          /profiles/currency-profile

        The body should be a JSON document that matches the schema for editing currencies

        OUTPUT:
         * Returns 204 if the currency is modified correctly
         * Returns 400 if the body of the request is not well formed or it is
           empty.
         * Returns 404 if there is no currency with messageid
         * Returns 415 if the input is not JSON.
         * Returns 500 if the database cannot be modified

        NOTE:
         * The attribute currencycode is for the column currencies.code
         * The attribute currencyname is fir the column currencies.name
        """

        #CHECK THAT Currency EXISTS
        if not g.con.get_curreny(currencyid):
            return create_error_response(404, "Currency not found",
                                         "There is no a currency with id %s" % currencyid
                                        )

        if JSON != request.headers.get("Content-Type",""):
            return create_error_response(415, "UnsupportedMediaType",
                                         "Use a JSON compatible format")
        request_body = request.get_json(force=True)
        #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:            
            currencycode = request_body["currencycode"]            
            currencyname = request_body["currencyname"]
			

        except KeyError:
            #This is launched if either currencycode or currencyname does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include currency_code  and currency_name")                                          
        else:
            #Modify the message in the database
            if not g.con.modify_currency(currencyid, currencycode, currencyname):
                return create_error_response(500, "Internal error",
                                         "Currency information for %s cannot be updated" % currencyid
                                        )
										
            return create_error_response(204, "Currency data modified",
                                         "Currency information for for currency with id  %s is updated successfully" % currencyid
                                        )
		
    def post(self, currencyid):
        """
        Adds a response to a currency with id <currencyid>.

        INPUT PARAMETERS:
       : param str currencyid: The id of the currency to be deleted

        REQUEST ENTITY BODY:
        * Media type: JSON
         * Profile: Updown_Currency
          /profiles/currency-profile

        The body should be a JSON document that matches the schema for new currency

        RESPONSE HEADERS:
         * Location: Contains the URL of the new currency

        RESPONSE STATUS CODE:
         * Returns 201 if the currency has been added correctly.
           The Location header contains the path of the new currency
         * Returns 400 if the currency is not well formed or the entity body is
           empty.
         * Returns 415 if the format of the response is not json
         * Returns 500 if the message could not be added to database.

         NOTE:
         * The attribute currencycode is  for the column currency.currency_code
         * The attribute currencyname is for the column currenecy.currency_name
        """

        return "eeeee"
		
		
api.add_resource(Currencies, "/updown/api/currencies/",
                 endpoint="currencies/")
				 
api.add_resource(Currency, "/updown/api/currency/<currencyid>",
                 endpoint="currency/")

if __name__ == '__main__':
    app.run(debug=True)

