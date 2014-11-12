INSERT INTO `auth_group` VALUES (4,'ascs'),(3,'customer'),(1,'dealers'),(2,'sas');

"run migrate dealer, asc and service advisor"

aftersell_ascsaveform (remove dealer fk)
insert into bajaj.bajaj_asctempregistration(id,name,password,phone_number,email,address,pincode,timestamp,dealer_id) select aftersell_ascsaveform.id, aftersell_ascsaveform.name, aftersell_ascsaveform.password, aftersell_ascsaveform.phone_number,aftersell_ascsaveform.email,aftersell_ascsaveform.address, aftersell_ascsaveform.pincode,aftersell_ascsaveform.timestamp, aftersell_ascsaveform.dealer_id  from aftersell_ascsaveform;

gladminds_sasaveform
insert into bajaj.bajaj_satempregistration(id,name,phone_number,status) select gladminds_sasaveform.id, gladminds_sasaveform.name, gladminds_sasaveform.phone_number,gladminds_sasaveform.status from gladminds_sasaveform;

aftersell_auditlog
insert into bajaj.bajaj_smslog(id, created_date, modified_date, action, message, sender, reciever) select aftersell_auditlog.id, aftersell_auditlog.date, aftersell_auditlog.date, aftersell_auditlog.action,aftersell_auditlog.message, aftersell_auditlog.sender, aftersell_auditlog.reciever from aftersell_auditlog;

aftersell_datafeedlog
insert into bajaj.bajaj_datafeedlog(data_feed_id, feed_type, total_data_count, failed_data_count, success_data_count, action, status, timestamp, remarks, file_location ) select aftersell_datafeedlog.data_feed_id, aftersell_datafeedlog.feed_type, aftersell_datafeedlog.total_data_count, aftersell_datafeedlog.failed_data_count, aftersell_datafeedlog.success_data_count, aftersell_datafeedlog.action, aftersell_datafeedlog.status, aftersell_datafeedlog.timestamp, aftersell_datafeedlog.remarks, aftersell_datafeedlog.file_location  from aftersell_datafeedlog;

gladminds_messagetemplate
insert into bajaj.bajaj_messagetemplate(id,template_key,template,description) select gladminds_messagetemplate.id, gladminds_messagetemplate.template_key, gladminds_messagetemplate.template, gladminds_messagetemplate.description from gladminds_messagetemplate;

gladminds_emailtemplate
insert into bajaj.bajaj_emailtemplate(id,template_key,sender,reciever,subject,body,description) select gladminds_emailtemplate.id, gladminds_emailtemplate.template_key, gladminds_emailtemplate.sender, gladminds_emailtemplate.reciever, gladminds_emailtemplate.subject, gladminds_emailtemplate.body, gladminds_emailtemplate.description from gladminds_emailtemplate;

gladminds_producttypedata
insert into bajaj.bajaj_producttype(product_type_id,product_name,product_type,image_url,is_active) select gladminds_producttypedata.product_type_id, gladminds_producttypedata.product_name, gladminds_producttypedata.product_type,gladminds_producttypedata.product_image_loc,gladminds_producttypedata.isActive from gladminds_producttypedata;

gladminds_branddata 

''' Write Script for these tables
aftersell_ucnrecovery 
id, reason, user_id, sap_customer_id, file_location, request_date, unique_service_coupon
id, created_date, modified_date, reason, customer_id, file_location, unique_service_coupon

gladminds_productdata| gladminds_gladmindusers
gladminds_coupondata  | gladminds_oldfscdata| gladminds_serviceadvisorcouponrelationship 
gladminds_customertempregistration'''

  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `gladmind_customer_id` varchar(215) DEFAULT NULL,
  `customer_name` varchar(215) NOT NULL,
  `email_id` varchar(215) DEFAULT NULL,
  `phone_number` varchar(15) NOT NULL,
  `registration_date` datetime NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `date_of_birth` varchar(255) DEFAULT NULL,
  `img_url` varchar(100) NOT NULL,
  `thumb_url` varchar(100) NOT NULL,
  `isActive` tinyint(1) NOT NULL,
  `accepted_terms` tinyint(1) NOT NULL,
  `gender` varchar(2) NOT NULL,
  `tshirt_size` varchar(2) NOT NULL,
  `pincode` varchar(15) DEFAULT NULL,


