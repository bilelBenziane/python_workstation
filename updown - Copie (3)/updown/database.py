'''
Created on 13.02.2013

Modified on 24.02.2018

Provides the database API to access the forum persistent data.

@author: ivan
@author: mika
'''

from datetime import datetime
import time, sqlite3, re, os
#Default paths for .db and .sql files to create and populate the database.
DEFAULT_DB_PATH = 'db/updown.db'
DEFAULT_SCHEMA = "db/updown_schema_dump.sql"
DEFAULT_DATA_DUMP = "db/updown_data_dump.sql"


class Engine(object):
    '''
    Abstraction of the database.

    It includes tools to create, configure,
    populate and connect to the sqlite file. You can access the Connection
    instance, and hence, to the database interface itself using the method
    :py:meth:`connection`.

    :Example:

    >>> engine = Engine()
    >>> con = engine.connect()

    :param db_path: The path of the database file (always with respect to the
        calling script. If not specified, the Engine will use the file located
        at *db/forum.db*

    '''
    def __init__(self, db_path=None):
        '''
        '''

        super(Engine, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = DEFAULT_DB_PATH

    def connect(self):
        '''
        Creates a connection to the database.

        :return: A Connection instance
        :rtype: Connection

        '''
        return Connection(self.db_path)

    def remove_database(self):
        '''
        Removes the database file from the filesystem.

        '''
        if os.path.exists(self.db_path):
            #THIS REMOVES THE DATABASE STRUCTURE
            os.remove(self.db_path)

    def clear(self):
        '''
        Purge the database removing all records from the tables. However,
        it keeps the database schema (meaning the table structure)

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        #THIS KEEPS THE SCHEMA AND REMOVE VALUES
        con = sqlite3.connect(self.db_path)
        #Activate foreing keys support
        cur = con.cursor()
        cur.execute(keys_on)
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM currencies")
            cur.execute("DELETE FROM users")
            cur.execute("DELETE FROM exchange")
            
    #METHODS TO CREATE AND POPULATE A DATABASE USING DIFFERENT SCRIPTS
    def create_tables(self, schema=None):
        '''
        Create programmatically the tables from a schema file.

        :param schema: path to the .sql schema file. If this parmeter is
            None, then *db/forum_schema_dump.sql* is utilized.

        '''
        con = sqlite3.connect(self.db_path)
        if schema is None:
            schema = DEFAULT_SCHEMA
        try:
            with open(schema, encoding="utf-8") as f:
                sql = f.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()

    def populate_tables(self, dump=None):
        '''
        Populate programmatically the tables from a dump file.

        :param dump:  path to the .sql dump file. If this parmeter is
            None, then *db/forum_data_dump.sql* is utilized.

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        con = sqlite3.connect(self.db_path)
        #Activate foreing keys support
        cur = con.cursor()
        cur.execute(keys_on)
        #Populate database from dump
        if dump is None:
            dump = DEFAULT_DATA_DUMP
        try:
            with open (dump, encoding="utf-8") as f:
                sql = f.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()

    #METHODS TO CREATE THE TABLES PROGRAMMATICALLY WITHOUT USING SQL SCRIPT
    def create_currencies_table(self):
        '''
        Create the table ``currencies`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
		
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE IF NOT EXISTS currencies(currency_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    currency_code TEXT UNIQUE, \
                    currency_name TEXT UNIQUE \
                    )'
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error as excp:
                print("Error %s:" % excp.args[0])
                return False
        return True

    def create_users_table(self):
        '''
        Create the table ``users`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
		
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    fullname TEXT, \
                    username TEXT UNIQUE, \
                    password TEXT \
                   )'
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error as excp:
                print("Error %s:" % excp.args[0])
                return False
        return True		
		
    def create_user_choice_table(self):
        '''
        Create the table ``user_choices`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''	
		
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE IF NOT EXISTS user_choices (choice_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    currency_id INTEGER, \
                    user_id INTEGER,\
                    from_currency INTEGER, \
                    to_currency INTEGER, \
                    date_from INTEGER, \
                    date_to INTEGER, \
                    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,  \
                    FOREIGN KEY(currency_id) REFERENCES currencies(currency_id) ON DELETE CASCADE \
                    )'
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error as excp:
                print("Error %s:" % excp.args[0])
                return False
        return True		
		
    def create_exchange_table(self):
        '''
        Create the table ``exchange`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''	
		
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE IF NOT EXISTS exchange(enentry_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    from_currency INTEGER, \
                    to_currency INTEGER, \
                    exact_date INTEGER, \
                    exchange_rate REAL, \
                    UNIQUE(from_currency, to_currency,exact_date), \
                    FOREIGN KEY(from_currency) REFERENCES currencies(currency_id) ON DELETE CASCADE, \
                    FOREIGN KEY(to_currency) REFERENCES currencies(currency_id) ON DELETE CASCADE \
                    )'
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error as excp:
                print("Error %s:" % excp.args[0])
                return False
        return True		


class Connection(object):
    '''
    API to access the updown database.

    The sqlite3 connection instance is accessible to all the methods of this
    class through the :py:attr:`self.con` attribute.

    An instance of this class should not be instantiated directly using the
    constructor. Instead use the :py:meth:`Engine.connect`.

    Use the method :py:meth:`close` in order to close a connection.
    A :py:class:`Connection` **MUST** always be closed once when it is not going to be
    utilized anymore in order to release internal locks.

    :param db_path: Location of the database file.
    :type dbpath: str

    '''
    def __init__(self, db_path):
        super(Connection, self).__init__()
        self.con = sqlite3.connect(db_path)
        self._isclosed = False

    def isclosed(self):
        '''
        :return: ``True`` if connection has already being closed.  
        '''
        return self._isclosed

    def close(self):
        '''
        Closes the database connection, commiting all changes.

        '''
        if self.con and not self._isclosed:
            self.con.commit()
            self.con.close()
            self._isclosed = True

    #FOREIGN KEY STATUS
    def check_foreign_keys_status(self):
        '''
        Check if the foreign keys has been activated.

        :return: ``True`` if  foreign_keys is activated and ``False`` otherwise.
        :raises sqlite3.Error: when a sqlite3 error happen. In this case the
            connection is closed.

        '''
        try:
            #Create a cursor to receive the database values
            cur = self.con.cursor()
            #Execute the pragma command
            cur.execute('PRAGMA foreign_keys')
            #We know we retrieve just one record: use fetchone()
            data = cur.fetchone()
            is_activated = data == (1,)
            print("Foreign Keys status: %s" % 'ON' if is_activated else 'OFF')
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            self.close()
            raise excp
        return is_activated

    def set_foreign_keys_support(self):
        '''
        Activate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        try:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            #execute the pragma command, ON
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    def unset_foreign_keys_support(self):
        '''
        Deactivate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.

        '''
        keys_on = 'PRAGMA foreign_keys = OFF'
        try:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            #execute the pragma command, OFF
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    #HELPERS
    #Here the helpers that transform database rows into dictionary. They work
    #similarly to ORM
    #this section is not necessary for the moment
	
    #Helpers for currencies
    def _create_currency_object(self, row):
        '''
        It takes a :py:class:`sqlite3.Row` and transform it into a dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary containing the following keys:

            * ``currency_id``: id of the currency (int)
            * ``currency_code``: currency's title
            * ``currencyname``: currency's name
            
            Note that all values in the returned dictionary are string unless
            otherwise stated.
        '''
        currency_id = row['currency_id']
        currency_code = row['currency_code']
        currency_name = row['currency_name']
        currency = {'currency_id': currency_id, 'currency_code': currency_code,
                   'currency_name': currency_name}
        return currency


    def _create_currencies_list_object(self, row):
        '''
        Same as :py:meth:`_create_currency_object`. However, the resulting
        dictionary is targeted to build currencies in a list.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the keys :
 
            * ``currency_id``: id of the currency (int)
            * ``currency_code``: currency's title
            * ``currency_name``: currency's name

        '''
        
        currency_id = row['currency_id']
        currency_code = row['currency_code']
        currency_name = row['currency_name']
        currency = {'curency_id': currency_id, 'currency_code': currency_code,
                   'currency_name': currency_name}
        return currency

    #Helpers for currencies
    def _create_user_object(self, row):
        '''
        It takes a :py:class:`sqlite3.Row` and transform it into a dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary containing the following keys:

            * ``user_id``: id of the user (int)
            * ``fullname``: user's full name
            * ``username``: user's name
            * ``password``: user's password
            
            Note that all values in the returned dictionary are string unless
            otherwise stated.
        '''
        user_id = row['user_id']
        fullname = row['fullname']
        username = row['username']
        password = row['password']
        user = {'user_id': user_id, 'fullname': fullname,
                    'username': username,'passord': password}
        return user	
	
    def _create_users_list_object(self, row):
        '''
        It takes a :py:class:`sqlite3.Row` and transform it into a dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary containing the following keys:

            * ``userid``: id of the user (int)
            * ``fullname``: user's full name
            * ``username``: user's name
            * ``password``: user's password
     
            
            Note that all values in the returned dictionary are string unless
            otherwise stated.
        '''
        user_id = row['user_id']
        fullname = row['fullname']
        username = row['username']
        password = row['password']
        user = {'user_id': user_id, 'fullname': fullname,
                    'username': username,'passord': password}
        return user	
		
    #Helpers for user_choices
    def _create_user_choices_list_object(self, row):
        '''
        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the keys :
 
            * ``choice_id``: id of the choice (int)
            * ``user_id``: user's id
            * ``from_currency``: currency's id
            * ``to_currency``: currency's id
            * ``date_from``: starting date
            * ``date_to``: ending date

        '''
        
        choice_id = row['choice_id']
        user_id = row['user_id']
        from_currency = row['from_currency']
        to_currency = row['to_currency']
        date_from = row['date_from']
        date_to = row['date_to']
        user_choices = {'choice_id': choice_id, 'user_id': user_id,
                   'from_currency': from_currency,'to_currency': to_currency,
				   'date_from': date_from,'date_to': date_to}
        return user_choices

    def _create_exchange_list_object(self, row):
        '''
        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the keys :
 
            * ``entry_id``: id of the entry (int)
            * ``from_currency``: currency's id
            * ``to_currency``: currency's id
            * ``date_from``: starting date
            * ``date_to``: ending date

        '''
        
        entry_id = row['entry_id']
        from_currency = row['from_currency']
        to_currency = row['to_currency']
        exact_date = row['exact_date']
        entry = {'entry_id': entry_id, 
                   'from_currency': from_currency,'to_currency': to_currency,
				   'exact_date': exact_date}
        return entry
		
    #API ITSELF
    #currencies Table API.
    def get_curreny(self, currencyid):
        '''
        Extracts a currency from the database.

        :param currencyid: The id of the currency. 
        :return: A dictionary with the format provided in
            :py:meth:`_create_currency_object` or None if the currency with target
            id does not exist.

        '''
        #Extracts the int which is the id for a message in the database
        
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the SQL Query
        query = 'SELECT * FROM currencies WHERE currency_id = ?'
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (currencyid,)
        cur.execute(query, pvalue)
        #Process the response.
        #Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        return self._create_currency_object(row)
	
    def get_all_currencies(self):
        '''
        Return a list of all the currencies in the database.

        :return: A list of currencies. Each currency is a dictionary containing
            the following keys:

            * ``currencyid``: string containing the currency id.
            * ``currencycode``:string containng code of the currency.
            * ``name``: string containing the name of the currency.

            Note that all values in the returned dictionary are string unless
            otherwise stated.

        '''
        #Create the SQL Statement build the string.
        query = 'SELECT * FROM currencies'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        currencies = []
        for row in rows:
            currency = self._create_currencies_list_object(row)
            currencies.append(currency)
        return currencies	
		
    def delete_currency(self, currencyid):
        '''
        Delete the currency with id given as parameter.

        :param str currencyid: id of the currency to remove.
        :return: True if the currency has been deleted, False otherwise

        '''
        #Create the SQL statment
        stmnt = 'DELETE FROM currencies WHERE currency_id = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (currencyid,)
        try:
            cur.execute(stmnt, pvalue)
            #Commit the currency
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)
		
    def modify_currency(self, currencyid, currencycode, currencyname):
        '''
        Modify the currency code_name and the name of the currency with id
        ``currencyid``

        :param int currencyid: The id of the currency to modify.
        :param str currencycode: the currency's code_name
        :param str currencyname: the currency's name
        :return: the id of the edited currency or None if the currency was
              not found.
        '''
        #Extracts the int which is the id for a currency in the database
        #Create the SQL statment
        stmnt = 'UPDATE currencies SET currency_code=:currency_code, currency_name=:currency_name\
                 WHERE currency_id =:currency_id'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = {"currency_code": currencycode,
                  "currency_name": currencyname,
                  "currency_id": currencyid}
        try:
            cur.execute(stmnt, pvalue)
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error %s:" % (e.args[0]))
        else: 
            if cur.rowcount < 1:
                return None
        return currencyid

    def create_currency(self, currencycode, currencyname):
        '''
        Create a new currency with the data provided as arguments.

        :param str currencycode: the currency's code_name
        :param str currencyname: the currency's name
        :return: the id of the created currency or None if the currency was not
            found.

        :raises ForumDatabaseError: if the database could not be modified.

        '''
        #Create the SQL statment
        #SQL Statement for inserting the data
        stmnt = 'INSERT INTO currencies (currency_code,currency_name ) \
                 VALUES(?,?)'
        #Variables for the statement.
        #currency_id is obtained from first statement.
        currency_id = None
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Generate the values for SQL statement
        pvalue = (currencycode, currencyname)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added message
        id = cur.lastrowid
        #Return the id in
        return id if id is not None else None

		
    #users Table API.
    def get_user(self, username):
        '''
        Extracts a currency from the database.

        :param username: The username of the user. 
        :return: A dictionary with the format provided in
            :py:meth:`_create_user_object` or None if the currency with target
            id does not exist.

        '''
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the SQL Query
        query = 'SELECT * FROM users WHERE username = ?'
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (username,)
        cur.execute(query, pvalue)
        #Process the response.
        #Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        return self._create_user_object(row)

    def get_all_users(self):
        '''
        Return a list of all the users in the database.

        :return: A dictionary with the format provided in
            :py:meth:`_create_users_object` or None if the currency with target
            id does not exist.
        '''
        #Create the SQL Statement build the string.
        query = 'SELECT * FROM users'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        users = []
        for row in rows:
            user = self._create_users_list_object(row)
            users.append(user)
        return users	
						
    def delete_user(self, username):
        '''
        Delete the currency with id given as parameter.

        :param str currencyid: id of the currency to remove.
        :return: True if the currency has been deleted, False otherwise

        '''
        #Create the SQL statment
        stmnt = 'DELETE FROM users WHERE username = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (username,)
        try:
            cur.execute(stmnt, pvalue)
            #Commit the currency
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)
		
		
    def modify_user(self, username, fullname, password):
        '''
        Modify the user fullname and password with username
        ``username``

        :param int username: The username of the user to modify.
        :param str fullname: the user's fullname
        :param str password: the user's password
        :return: the username of the edited currency or None if the currency was
              not found.
        '''
        #Extracts the int which is the id for a currency in the database
        #Create the SQL statment
        stmnt = 'UPDATE users SET fullname=:fullname, password=:password\
                 WHERE username =:username'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = {"fullname": fullname,
                  "password": password,
                  "username": username}
        try:
            cur.execute(stmnt, pvalue)
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error %s:" % (e.args[0]))
        else: 
            if cur.rowcount < 1:
                return None
        return username

    def create_user(self,fullname, username, password):
        '''
        Create a new user with the data provided as arguments.

        :param str username: the user's username
        :param str fullname: the user's fullname
        :param str password: the user's password
        :return: the username of the created currency or None if the currency was not
            found.

        :raises UpDownDatabaseError: if the database could not be modified.

        '''
        #Create the SQL statment
        #SQL Statement for inserting the data
        stmnt = 'INSERT INTO users (username,fullname,password ) \
                 VALUES(?,?,?)'
        #Variables for the statement.
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Generate the values for SQL statement
        pvalue = (username, fullname,password)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added user
        id = cur.lastrowid
        #Return the username
        if id is not None :
           	return username	
        else :
            return None		

    def add_user_choice(self, username,from_currency,to_currency,date_from=0,date_to=0):
        '''
        add a new choice with the data provided as arguments.

        :param str username: the user's username
        :param int from_currency: the currency's to convert from
        :param int to_currency: the currency's to convert to
        :param int date_from: starting date param
        :param int date_to: end date param
        :return: the id of the entry or None if the currency was not
            found.

        :raises ForumDatabaseError: if the database could not be modified.

        '''
        #Get user id
        user_id=self.get_user_id(username)
        if user_id is None :
            return None		
        #Create the SQL statment
        #SQL Statement for inserting the data
        stmnt = 'INSERT INTO user_choices (user_id,from_currency,to_currency,date_from,date_to ) \
                 VALUES(?,?,?,?,?)'
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Generate the values for SQL statement
        pvalue = (user_id,from_currency,to_currency,date_from,date_to)
        #Activate foreign key support
        self.set_foreign_keys_support()        
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added message
        id = cur.lastrowid
        #Return the id in
        return id if id is not None else None

    def delete_user_choice(self, username,from_currency,to_currency,date_from,date_to):
        '''
        Delete the currency with id given as parameter.

        :param str currencyid: id of the currency to remove.
        :return: True if the currency has been deleted, False otherwise

        '''
        #Get user id
        user_id=self.get_user_id(username)
        if user_id is None :
            return None		
        #Create the SQL statment
        stmnt = 'DELETE FROM user_choices WHERE user_id = ? AND from_currency=? AND to_currency=? AND date_from=? AND date_to=?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (user_id,from_currency,to_currency,date_from,date_to)
        try:
            cur.execute(stmnt, pvalue)
            #Commit the currency
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)
		
    def get_user_choices(self, username):
        '''
        Extracts a currency from the database.

        :param username: The username of the user. 
        :return: A dictionary with the format provided in
            :py:meth:`_create_currencies_object` or None if the currency with target
            id does not exist.

        '''
        #Get user id
        user_id=self.get_user_id(username)
        if user_id is None :
            return None		
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the SQL Query
        query = 'SELECT * FROM user_choices WHERE user_id = ?'
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (user_id,)
        cur.execute(query, pvalue)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        users = []
        for row in rows:
            user = self._create_user_choices_list_object(row)
            users.append(user)
        return users	
				
    #exchange Table API.
    def get_exchange(self, from_currency,to_currency,date_from,date_to):
        '''
        Extracts a currency from the database.

        :param username: The username of the user. 
        :return: A dictionary with the format provided in
            :py:meth:`_create_currencies_object` or None if the currency with target
            id does not exist.

        '''
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the SQL Query
        #query = 'SELECT * FROM exchange WHERE from_currency = ? AND to_currency=? AND exact_date >= ? AND exact_date <= ? '
        query = 'SELECT * FROM exchange '
        if from_currency != 1 or to_currency != 1 or date_from != 0 or date_to != 0 :
            query += 'WHERE '
        if from_currency != 1 :
            query += " from_currency = '%s'" % from_currency
        if to_currency != 1 :
            if from_currency != 1 :
                query +=' AND'			
            query += " to_currency = '%s'" % to_currency
        if date_from != 0 :
            if from_currency != 1 or to_currency != 1:
                query +=' AND'			
            query += " exact_date >= '%s'" % date_from
        if date_to != 0 :
            if from_currency != 1 or to_currency != 1 or date_from !=0:
                query +=' AND'			
            query += " exact_date <= '%s'" % date_to
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (from_currency,to_currency,date_from,date_to,)
        #cur.execute(query, pvalue)
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        choices = []
        for row in rows:
            choice = self._create_exchange_list_object(row)
            choices.append(choice)
        return choices	

    def add_exchange(self, from_currency,to_currency,exact_date,exchange_rate):
        '''
        add a new exchange rate with the data provided as arguments.

        :param int from_currency: the currency's to convert from
        :param int to_currency: the currency's to convert to
        :param int exact_date: date of the changing rate
        :param Real rate: exchange rate
        :return: the id of the entry or None if the currency was not
            found.

        :raises ForumDatabaseError: if the database could not be modified.

        '''
        #Create the SQL statment
        #SQL Statement for inserting the data
        stmnt = 'INSERT INTO exchange (from_currency,to_currency,exact_date,exchange_rate ) \
                 VALUES(?,?,?,?)'
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Generate the values for SQL statement
        pvalue = (from_currency,to_currency,exact_date,exchange_rate)
        #Activate foreign key support
        self.set_foreign_keys_support()        
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added entry
        id = cur.lastrowid
        #Return the id in
        return id if id is not None else None
		
    # UTILS
    def get_user_id(self, username):
        '''
        Get the key of the database row which contains the user with the given
        username.

        :param str username: The username of the user to search.
        :return: the database attribute user_id or None if ``nickname`` does
            not exit.
        :rtype: str

        '''
        query = 'SELECT user_id FROM users WHERE username = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the  main SQL statement
        pvalue = (username,)
        cur.execute(query, pvalue)
        #Process the response.
        #Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        else:
            return row[0]
