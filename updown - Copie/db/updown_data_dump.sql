/*	Seeding some Data to test the functionalities of the tables : */

/* Currencies data : */
INSERT INTO "currencies" VALUES(1,'USD','United States Dollar');
INSERT INTO "currencies" VALUES(2,'BTC','Bitcoin');
INSERT INTO "currencies" VALUES(3,'EURO','EURO');
INSERT INTO "currencies" VALUES(4,'GBP','Pound sterling');
INSERT INTO "currencies" VALUES(5,'ETH','Ethereum');


/* Users data : */
INSERT INTO "users" VALUES(1,'Nadir Redouane Hamza','NRH','9IIW',1,3,20180214,20180728);
INSERT INTO "users" VALUES(2,'katia dandou cavi','KDC','KIWI',3,1,20180114,20180730);


/* Exchange data : */
INSERT INTO "exchange" VALUES(1,1,3,20180219,1.45);
INSERT INTO "exchange" VALUES(2,1,3,20180220,1.5);
INSERT INTO "exchange" VALUES(3,1,3,20180221,1.7);
INSERT INTO "exchange" VALUES(4,1,3,20180222,1.9);
		 