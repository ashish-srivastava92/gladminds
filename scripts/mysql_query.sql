mysql -u gladminds -pgladminds123
use gladmindsdb;

-------------------------create dump---------------------------
mysqldump -u gladminds -p gladmindsdb -r gladmindsdb.sql
--terminal command

-------------------------create dump---------------------------

-------------------------create copy---------------------------
mysqldump -u gladminds -pgladminds123 gladmindsdb > gladmindsdb_dump.sql
mysql -u gladminds -pgladminds123;

CREATE DATABASE gladmindsdb_4apr;

USE gladmindsdb_copy;

SOURCE gladmindsdb.sql;
-------------------------create copy-------------------------------

mysqldump -uroot -prootpassword > gmdbcopy5may.sql

-------------------------create copy-------------------------------

----------------------------RDS Data Import-----------------------
mysqldump -h gladminds-qa.chnnvvffqwop.us-east-1.rds.amazonaws.com  -u gladminds -pgladminds123 gladmindsdbqa > gladminds_db.sql 

--------------------------------------------------------------------
-------------------------other changes---------------------------

ALTER TABLE gladminds_serviceadvisor ADD status CHAR(10) NOT NULL DEFAULT 'y';
ALTER TABLE gladminds_productdata ADD engine CHAR(255);
desc gladminds_productdata;

Create Index vin_idx on gladminds_coupondata(vin_id);
Create Index closed_date_vin_idx on gladminds_coupondata(closed_date, vin_id);

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

----------------Migration Script for 1.3 ----------------------------
ALTER TABLE gladminds_coupondata ADD extended_date DATETIME DEFAULT NULL;
CREATE TABLE `gladminds_serviceadvisorcouponrelationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unique_service_coupon_id` int(11) NOT NULL,
  `service_advisor_phone_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gladminds_serviceadvisorcouponrelationship_49ac3df4` (`unique_service_coupon_id`),
  KEY `gladminds_serviceadvisorcouponrelationship_85d2f9c5` (`service_advisor_phone_id`),
  CONSTRAINT `service_advisor_phone_id_refs_id_ff3268c1` FOREIGN KEY (`service_advisor_phone_id`) REFERENCES `gladminds_serviceadvisor` (`id`),
  CONSTRAINT `unique_service_coupon_id_refs_id_862689b3` FOREIGN KEY (`unique_service_coupon_id`) REFERENCES `gladminds_coupondata` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-------------------Migration Script for 1.3.1 ------------------
--
-- Table structure for table `auth_group`
--
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

LOCK TABLES `auth_group` WRITE;
INSERT INTO `auth_group` VALUES (4,'ascs'),(3,'customer'),(1,'dealers'),(2,'sas');
UNLOCK TABLES;


-------------------create slow query log------------------

sudo mkdir /var/log/mysql
sudo touch /var/log/mysql/log-slow-queries.log
sudo chown mysql.mysql -R /var/log/mysql

set global slow_query_log = 'ON';
set global slow_query_log_file = '/var/log/mysql/log-slow-queries.log';
show variables like '%slow%';

-------------------create slow query log------------------



------------------------create user in mysql---------------------
+CREATE USER 'gladminds'@'localhost' IDENTIFIED BY 'gladmindsRocks';
+GRANT ALL PRIVILEGES ON *.* TO 'gladminds'@'localhost';
----------------------------------------------------------


-------------------- DB size in MB --------------------------------
SELECT table_schema  gladmindsdb, 
   Round(Sum(data_length + index_length) / 1024 / 1024, 1) "DB Size in MB" 
FROM   information_schema.tables 
GROUP  BY table_schema;
------------------------------------------------------------------------


----------------------------Mysql data fetch query---------------------

SELECT gladminds_productdata.vin, gladminds_productdata.sap_customer_id, gladminds_gladmindusers.phone_number, gladminds_gladmindusers.customer_name
FROM gladminds_productdata
INNER JOIN gladminds_gladmindusers
ON gladminds_productdata.customer_phone_number_id=gladminds_gladmindusers.id;

 
----------------------------------------------------------------------
