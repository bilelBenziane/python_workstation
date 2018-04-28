PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
/*Table for list of currencies*/
CREATE TABLE IF NOT EXISTS currencies (
  currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
  code_name TEXT UNIQUE,
  name TEXT
);

/*Table to store users' Settings*/
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  fullname TEXT,
  username TEXT UNIQUE,
  password TEXT,
  from_currency INTEGER,
  to_currency INTEGER,
  date_from INTEGER,
  date_to INTEGER,
  FOREIGN KEY(from_currency) REFERENCES currencies(currency_id) ON DELETE SET NULL,
  FOREIGN KEY(to_currency) REFERENCES currencies(currency_id) ON DELETE SET NULL 
);

/*Table for exchange rate entries*/
CREATE TABLE IF NOT EXISTS exchange(
		  entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
		  from_currency INTEGER,
		  to_currency INTEGER,
		  exact_date INTEGER,
		  exchange_rate REAL,
		  UNIQUE(from_currency, to_currency,exact_date),
		  FOREIGN KEY(from_currency) REFERENCES currencies(currency_id) ON DELETE SET NULL,
		  FOREIGN KEY(to_currency) REFERENCES currencies(currency_id) ON DELETE SET NULL
);
  
COMMIT;
PRAGMA foreign_keys=ON;

