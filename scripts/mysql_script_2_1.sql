INSERT INTO `auth_group` VALUES (4,'ascs'),(3,'customer'),(1,'dealers'),(2,'sas');

"run migrate dealer, asc and service advisor"

insert into bajaj.bajaj_asctempregistration(id,name,password,phone_number,email,address,pincode,timestamp,dealer_id) select aftersell_ascsaveform.id, aftersell_ascsaveform.name, aftersell_ascsaveform.password, aftersell_ascsaveform.phone_number,aftersell_ascsaveform.email,aftersell_ascsaveform.address, aftersell_ascsaveform.pincode,aftersell_ascsaveform.timestamp, aftersell_ascsaveform.dealer_id  from aftersell_ascsaveform;

insert into bajaj.bajaj_satempregistration(id,name,phone_number,status) select gladminds_sasaveform.id, gladminds_sasaveform.name, gladminds_sasaveform.phone_number,gladminds_sasaveform.status from gladminds_sasaveform;

insert into bajaj.bajaj_smslog(id, created_date, modified_date, action, message, sender, receiver, status) select aftersell_auditlog.id, aftersell_auditlog.date, aftersell_auditlog.date, aftersell_auditlog.action,aftersell_auditlog.message, aftersell_auditlog.sender, aftersell_auditlog.reciever,aftersell_auditlog.status from aftersell_auditlog;

insert into bajaj.bajaj_datafeedlog(data_feed_id, feed_type, total_data_count, failed_data_count, success_data_count, action, status, timestamp, remarks, file_location ) select aftersell_datafeedlog.data_feed_id, aftersell_datafeedlog.feed_type, aftersell_datafeedlog.total_data_count, aftersell_datafeedlog.failed_data_count, aftersell_datafeedlog.success_data_count, aftersell_datafeedlog.action, aftersell_datafeedlog.status, aftersell_datafeedlog.timestamp, aftersell_datafeedlog.remarks, aftersell_datafeedlog.file_location  from aftersell_datafeedlog;

insert into bajaj.bajaj_messagetemplate(id,template_key,template,description) select gladminds_messagetemplate.id, gladminds_messagetemplate.template_key, gladminds_messagetemplate.template, gladminds_messagetemplate.description from gladminds_messagetemplate;

insert into bajaj.bajaj_emailtemplate(id,template_key,sender,receiver,subject,body,description) select gladminds_emailtemplate.id, gladminds_emailtemplate.template_key, gladminds_emailtemplate.sender, gladminds_emailtemplate.reciever, gladminds_emailtemplate.subject, gladminds_emailtemplate.body, gladminds_emailtemplate.description from gladminds_emailtemplate;

insert into bajaj.bajaj_producttype(id,product_type,image_url,is_active) select gladminds_producttypedata.product_type_id, gladminds_producttypedata.product_type,gladminds_producttypedata.product_image_loc,gladminds_producttypedata.isActive from gladminds_producttypedata;

alter table bajaj_oldfscdata change `product_id` `product_id` int(11) default null;

'''
set the env varibales (QA)

export DB_USER='gladminds'
export DB_PASSWORD='gladmindsqa2'
export DB_HOST='gladminds-qa-2.chnnvvffqwop.us-east-1.rds.amazonaws.com'
export MIGRATE_DB='gladminds'
export OFFSET=0

Run these commands
nohup python scripts/migrate_dealer_data.py &
nohup python scripts/migrate_asc_data.py &
nohup python scripts/migrate_service_advisor.py &
'''

use bajaj;


insert into bajaj_productdata(
id,created_date,modified_date,product_id,customer_id,
customer_phone_number,customer_name,customer_city, customer_state, customer_pincode,
purchase_date,invoice_date,engine,veh_reg_no,is_active,
product_type_id,dealer_id_id)
select p.id, p.created_on, p.last_modified, p.vin as product_id, p.sap_customer_id, 
u.phone_number, u.customer_name, u.address, u.state, u.pincode,
p.product_purchase_date, p.invoice_date, p.engine, p.veh_reg_no, p.isActive,
p.product_type_id, new_dealer.user_id
from gladminds.gladminds_productdata p
inner join gladminds.aftersell_registereddealer old_dealer on p.dealer_id_id = old_dealer.id
inner join bajaj.bajaj_dealer new_dealer on old_dealer.dealer_id = new_dealer.dealer_id
left outer join gladminds.gladminds_gladmindusers u on p.customer_phone_number_id = u.id; 

'''Query OK, 3937716 rows affected (3 min 43.85 sec)
Records: 3937716  Duplicates: 0  Warnings: 0'''

insert into bajaj_coupondata(
id, unique_service_coupon, valid_days, valid_kms, service_type, status,
closed_date, mark_expired_on, actual_service_date, actual_kms, last_reminder_date,
schedule_reminder_date, extended_date, sent_to_sap,
credit_date, credit_note, special_case, product_id, service_advisor_id
)
select p.id, p.unique_service_coupon, p.valid_days, p.valid_kms, p.service_type, p.status,
p.closed_date, p.mark_expired_on, p.actual_service_date,p.actual_kms, p.last_reminder_date,
p.schedule_reminder_date, p.extended_date, p.sent_to_sap,
p.credit_date, p.credit_note, p.special_case, p.vin_id, new_sa.user_id
from gladminds.gladminds_coupondata p
left outer join gladminds.aftersell_serviceadvisor old_sa on p.sa_phone_number_id = old_sa.id
left outer join bajaj.bajaj_serviceadvisor new_sa on old_sa.service_advisor_id = new_sa.service_advisor_id;

'''Query OK, 8655736 rows affected, 2 warnings (7 min 26.12 sec)
Records: 8655736  Duplicates: 0  Warnings: 2'''


'''
nohup python scripts/migrate_coupons_sa_relations.py &

nohup python scripts/migrate_old_fsc.py &
nohup python scripts/migrate_temp_customer.py &
nohup python scripts/migrate_ucn_recovery.py &
'''

