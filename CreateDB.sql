create schema ration_store_group31;
use ration_store_group31;

CREATE TABLE PRODUCTS (
    prodid smallint PRIMARY KEY NOT NULL auto_increment,
    prodname VARCHAR(15),
    mrp FLOAT,
    stock FLOAT
);
alter table products auto_increment=1001;

CREATE TABLE SUBSIDY (
    prodid smallint,
    category CHAR(5),
    discount FLOAT,
    maximum FLOAT,
    PRIMARY KEY (prodid , category),
    FOREIGN KEY (prodid)
        REFERENCES products (prodid),
	check(category in ("BPL-1","BPL-2"))
);

CREATE TABLE UNITS (
    batchno smallint PRIMARY KEY NOT NULL auto_increment,
    prodid smallint,
    dom DATE,
    expiry DATE,
    size FLOAT,
    FOREIGN KEY (prodid)
        REFERENCES products (prodid)
);
alter table units auto_increment=4501;

CREATE TABLE CUSTOMERS (
    custid smallint PRIMARY KEY NOT NULL auto_increment,
    name CHAR(15),
    category VARCHAR(5),
    phone BIGINT UNIQUE,
    check(category in ("APL", "BPL-1","BPL-2"))
);
alter table customers auto_increment=2001;

CREATE TABLE CARDDETAILS (
    custid smallint PRIMARY KEY NOT NULL,
    cardno mediumint UNIQUE,
    members smallint,
    claimed BOOL,
    FOREIGN KEY (custid)
        REFERENCES customers (custid)
);

CREATE TABLE ORDERS (
    ordid mediumint PRIMARY KEY NOT NULL auto_increment,
    custid smallint,
    date DATE,
    FOREIGN KEY (custid)
        REFERENCES customers (custid)
);
alter table orders auto_increment=404001;

CREATE TABLE ORDERDETAILS (
    ordid mediumint,
    prodid smallint,
    quantity FLOAT,
    FOREIGN KEY (ordid)
        REFERENCES orders (ordid),
    FOREIGN KEY (prodid)
        REFERENCES products (prodid)
);
