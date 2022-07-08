insert into products (prodname,mrp,stock) values
("Wheat",25,300),
("Rice",35,200),
("Sugar",40,75),
("Kerosene",28,50),
("Maize",18,150);

insert into customers (name,category,phone) values
("Alpha","APL",9876500101),
("Beta","BPL-1",9876500102),
("Gamma","BPL-2",9876500103),
("Delta","APL",9876500104),
("Lambda","BPL-1",9876500105);
create or replace view useful as select * from units where prodid = 1001;
create or replace view old as select * from useful where expiry = (select min(expiry) from useful);
select * from useful;
select min(size) from old;
select batchno from old where size = (select min(size) from old);
insert into carddetails values
(2002,747102,6,1),
(2003,747103,4,1),
(2005,747105,5,0);

insert into units (prodid,dom,expiry,size) values
(1001,"2021-02-25","2021-08-26",100),
(1001,"2021-03-12","2021-09-13",100),
(1001,"2021-03-29","2021-09-30",100),
(1002,"2021-03-01","2021-09-02",100),
(1002,"2021-03-10","2021-09-11",100),
(1003,"2021-02-17","2021-09-18",25),
(1003,"2021-03-13","2021-10-14",50),
(1004,"2021-01-07","2022-01-08",25),
(1004,"2021-02-14","2022-02-15",25),
(1005,"2021-03-19","2022-07-20",100),
(1005,"2021-03-28","2021-07-29",50);

insert into subsidy values
(1001,"BPL-1",90,10),
(1002,"BPL-1",85,8),
(1003,"BPL-1",80,5),
(1004,"BPL-1",95,5),
(1005,"BPL-1",80,6),
(1001,"BPL-2",80,15),
(1002,"BPL-2",70,10),
(1003,"BPL-2",75,9),
(1004,"BPL-2",60,10),
(1005,"BPL-2",75,8);

insert into orders (custid, date) values
(2001,"2021-04-02"),
(2002,"2021-04-03"),
(2003,"2021-04-04");

insert into orderdetails values
(404001,1001,25),
(404001,1003,11),
(404002,1001,55),
(404002,1002,40),
(404002,1004,20),
(404003,1002,32),
(404003,1005,25);

update products set stock=220 where prodid=1001;
update products set stock=128 where prodid=1002;
update products set stock=64 where prodid=1003;
update products set stock=30 where prodid=1004;
update products set stock=125 where prodid=1005;

update units set size=20 where batchno=4501;
update units set size=28 where batchno=4504;
update units set size=14 where batchno=4506;
update units set size=5 where batchno=4508;
update units set size=75 where batchno=4510;
