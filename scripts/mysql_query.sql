mysql -u gladminds -pgladminds123
use gladmindsdb;

-------------------------create dump---------------------------
mysqldump -u gladminds -p gladmindsdb -r gladmindsdb.sql
--terminal command

-------------------------create dump---------------------------

-------------------------create copy---------------------------
mysqldump -u gladminds -pgladminds123 gladmindsdb > gladmindsdb_dump.sql
mysql -u gladminds -pgladminds123;

CREATE DATABASE gladmindsdb_copy;

USE gladmindsdb_copy;

SOURCE gladmindsdb.sql;
-------------------------create copy-------------------------------


-------------------------other changes---------------------------

ALTER TABLE gladminds_serviceadvisor ADD status CHAR(10) NOT NULL DEFAULT 'y';
ALTER TABLE gladminds_productdata ADD engine CHAR(255);
desc gladminds_productdata;

-------------------------other changes---------------------------


----------------delete DB data----------------------------
delete from gladminds_coupondata;
delete from gladminds_productdata;
delete from gladminds_producttypedata;
delete from datafeedlog;
delete from gladminds_auditlog;

----------------delete DB data----------------------------

----------------Migration Script for 1.2 ----------------------------
use gladmindsdb;
select  * from  gladminds_serviceadvisor;

ALTER TABLE gladminds_serviceadvisor DROP status;
show create table gladminds_serviceadvisor; 
ALTER TABLE gladminds_serviceadvisor DROP FOREIGN KEY fk_symbol;
ALTER TABLE gladminds_serviceadvisor DROP dealer_id_id;


CREATE TABLE gladminds_serviceadvisordealerrelationship(
    status CHAR(10) NOT NULL
);


ALTER TABLE gladminds_serviceadvisordealerrelationship ADD FOREIGN KEY (`dealer_id`) REFERENCES gladminds_registereddealer(`dealer_id`);


----------------Migration Script for 1.2 ----------------------------

