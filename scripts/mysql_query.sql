mysql -u gladminds -pgladminds123
use gladmindsdb;


mysqldump -u gladminds -p gladmindsdb -r gladmindsdb.sql

mysql -u gladminds -pgladminds123;

CREATE DATABASE gladmindsdb_copy;

USE gladmindsdb_copy;

SOURCE gladmindsdb.sql;

ALTER TABLE gladminds_serviceadvisor ADD status CHAR(10) NOT NULL DEFAULT 'y';
ALTER TABLE gladminds_productdata ADD engine CHAR(255);
desc gladminds_productdata;
