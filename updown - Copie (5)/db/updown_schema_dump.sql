PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
/*Table for list of currencies*/
CREATE TABLE IF NOT EXISTS currencies (
  currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
  currency_code TEXT UNIQUE,
  currency_name TEXT UNIQUE
);

/*Table to store users*/
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  fullname TEXT,
  username TEXT UNIQUE,
  password TEXT
  );

/*Table to store users' parameters*/
CREATE TABLE IF NOT EXISTS user_choices (
  choice_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  from_currency INTEGER,
  to_currency INTEGER,
  date_from INTEGER,
  date_to INTEGER,
  UNIQUE(from_currency, to_currency,user_id),
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE, 
  FOREIGN KEY(from_currency) REFERENCES currencies(currency_id) ON DELETE CASCADE,
  FOREIGN KEY(to_currency) REFERENCES currencies(currency_id) ON DELETE CASCADE  
);

/*Table for exchange rate entries*/
CREATE TABLE IF NOT EXISTS exchange(
		  entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
		  from_currency INTEGER,
		  to_currency INTEGER,
		  exact_date INTEGER,
		  exchange_rate REAL,
		  UNIQUE(from_currency, to_currency,exact_date),
		  FOREIGN KEY(from_currency) REFERENCES currencies(currency_id) ON DELETE CASCADE,
		  FOREIGN KEY(to_currency) REFERENCES currencies(currency_id) ON DELETE CASCADE
);
  
COMMIT;
PRAGMA foreign_keys=ON;

