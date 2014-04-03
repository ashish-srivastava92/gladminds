mysql -u gladminds -pgladminds123
use gladmindsdb;

-------------------------create dump---------------------------
mysqldump -u gladminds -p gladmindsdb -r gladmindsdb.sql
--terminal command
mysqldump -u gladminds -pgladminds123 gladmindsdb > gladmindsdb_dump.sql
-------------------------create dump---------------------------

-------------------------create copy---------------------------
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
