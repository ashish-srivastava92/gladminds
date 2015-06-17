-- First create database gladminds_qa in local using the qa dump


-- In 'gm' Database :
delete from auth_user;
insert into gm.auth_user select * from gladminds_qa.auth_user;
insert into gm.auth_group select * from gladminds_qa.auth_group;
delete from auth_permission;
insert into gm.auth_permission select * from gladminds_qa.auth_permission;
insert into gm.auth_user_user_permissions select * from gladminds_qa.auth_user_user_permissions;
insert into gm.auth_user_groups select * from gladminds_qa.auth_user_groups;
insert into gm.gm_otptoken select * from gladminds_qa.gladminds_otptoken;

-- Run this in gladminds_qa DB

CREATE TABLE `gladminds_userprofile` (
  `user_id` int(11) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `profile_pic` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_id_refs_id_9c5ad4ad` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
)

-- Run the python script migrate_users.py 
-- python migrate_users.py
--------- Run this in 'gm' database

insert into gm.gm_userprofile select * from gladminds_qa.gladminds_userprofile;
insert into gm.gm_gladmindusers (id, gladmind_customer_id,customer_name,email_id,phone_number,registration_date,address,country,state,date_of_birth, gender, img_url,thumb_url,isActive,pincode,user_id) select id, gladmind_customer_id,customer_name,email_id,phone_number,registration_date,address,country,state,date_of_birth, gender, img_url,thumb_url,isActive,pincode,user_id from gladminds_qa.gladminds_gladmindusers;


-- In bajaj db

insert into bajaj.auth_group select * from gladminds_qa.auth_group;
insert into bajaj.auth_user_groups select * from gladminds_qa.auth_user_groups;
insert into bajaj.bajaj_ascsaveform select * from gladminds_qa.aftersell_ascsaveform;
insert into bajaj.bajaj_registereddealer select * from gladminds_qa.aftersell_registereddealer;
insert into bajaj.bajaj_serviceadvisor select * from gladminds_qa.aftersell_serviceadvisor;
insert into bajaj.bajaj_uploadproductcsv select * from gladminds_qa.gladminds_uploadproductcsv;
insert into bajaj.bajaj_branddata select * from gladminds_qa.gladminds_branddata;
insert into bajaj.bajaj_productinsuranceinfo select * from gladminds_qa.gladminds_productinsuranceinfo;
insert into bajaj.bajaj_productwarrantyinfo select * from gladminds_qa.gladminds_productwarrantyinfo;
insert into bajaj.bajaj_sparesdata select * from gladminds_qa.gladminds_sparesdata;
insert into bajaj.bajaj_producttypedata (product_type_id,brand_id_id, product_name,product_type, product_image_loc,isActive) select product_type_id,1, product_name,product_type, product_image_loc,isActive from gladminds_qa.gladminds_producttypedata;
insert into bajaj.bajaj_messagetemplate select * from gladminds_qa.gladminds_messagetemplate;
insert into bajaj.bajaj_emailtemplate select * from gladminds_qa.gladminds_emailtemplate;
insert into bajaj.bajaj_sasaveform select * from gladminds_qa.gladminds_sasaveform;

--- Run script ucn_recovery.py
-- In bajaj db
insert into bajaj.bajaj_ucnrecovery select * from gladminds_qa.aftersell_ucnrecovery;

-- Run the python script migrate_products.py
 python migrate_products.py
-- Run script migrate_coupons.py
 python migrate_coupons.py

insert into bajaj.bajaj_serviceadvisorcouponrelationship select * from gladminds_qa.aftersell_serviceadvisorcouponrelationship;
insert into bajaj.bajaj_customertempregistration select * from gladminds_qa.aftersell_customertempregistration;

