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

mkdir /var/log/mysql
touch /var/log/mysql/log-slow-queries.log
chown mysql.mysql -R /var/log/mysql

set global slow_query_log = 'ON';
set global slow_query_log_file = '/var/log/mysql/log-slow-queries.log;
show variables like '%slow%';

Create Index closed_date_vin_idx on gladminds_coupondata(closed_date, vin_id);
