/*	Seeding some Data to test the functionalities of the tables : */

/* currencies data : */
INSERT INTO "currencies" VALUES(1,'USD','United States Dollar');
INSERT INTO "currencies" VALUES(2,'BTC','Bitcoin');
INSERT INTO "currencies" VALUES(3,'EURO','EURO');
INSERT INTO "currencies" VALUES(4,'GBP','Pound sterling');
INSERT INTO "currencies" VALUES(5,'ETH','Ethereum');


/* users data : */
INSERT INTO "users" VALUES(1,'Nadir bengana','nadiro','9IIW');
INSERT INTO "users" VALUES(2,'Zair Hamza ','hamzou','9IIWI');
INSERT INTO "users" VALUES(3,'Redouane Kaddari ','redone','KIWI');


/*exchange data : */
INSERT INTO "exchange" VALUES(1,1,3,20180219,1.45);
INSERT INTO "exchange" VALUES(2,1,3,20180220,1.5);
INSERT INTO "exchange" VALUES(3,1,3,20180221,1.7);
INSERT INTO "exchange" VALUES(4,1,3,20180222,1.9);
INSERT INTO "exchange" VALUES(5,2,4,20180219,1.45);
INSERT INTO "exchange" VALUES(6,2,4,20180220,1.5);
INSERT INTO "exchange" VALUES(7,2,4,20180221,1.7);
INSERT INTO "exchange" VALUES(8,2,4,20180222,1.9);


/* user_choices data : */
INSERT INTO "user_choices" VALUES(1,1,1,3,20180220,20180222);
INSERT INTO "user_choices" VALUES(2,1,1,3,20180220,20180221);
INSERT INTO "user_choices" VALUES(3,3,2,4,20180220,20180221);
INSERT INTO "user_choices" VALUES(4,3,2,4,20180220,20180221);

		 

