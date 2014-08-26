##First load DB from dump
##Then sync DB
#####################script for prod_1_3_1----------------
insert into aftersell_ascsaveform (select * from gladminds_ascsaveform);
insert into aftersell_auditlog (select * from gladminds_auditlog);

alter table gladminds_datafeedlog  add remarks varchar(2048) null;
ALTER TABLE gladminds_datafeedlog  ADD file_location  VARCHAR(215);
insert into aftersell_datafeedlog (select * from gladminds_datafeedlog);

insert into aftersell_registereddealer (select * from gladminds_registereddealer);
insert into aftersell_serviceadvisor (select * from gladminds_serviceadvisor);
insert into aftersell_serviceadvisordealerrelationship (select * from gladminds_serviceadvisordealerrelationship);

 
#####Syncdb will add new registered ASC Table
drop table gladminds_registeredasc;
drop table gladminds_ascsaveform;
drop table gladminds_auditlog;
drop table gladminds_datafeedlog;
drop table gladminds_serviceadvisordealerrelationship;

alter table gladminds_productdata  add foreign key (dealer_id_id) references aftersell_registereddealer(id);

###(to get the foreign key name)
show create table gladminds_productdata; 

###(dealer_id_id_refs_id_a8be2be4 this is foreign key name)
alter table gladminds_productdata drop foreign key  dealer_id_id_refs_id_a8be2be4; 

drop table gladminds_registereddealer;


alter table gladminds_serviceadvisorcouponrelationship  add foreign key (service_advisor_phone_id) references aftersell_serviceadvisor(id);
show create table gladminds_serviceadvisorcouponrelationship;
alter table gladminds_serviceadvisorcouponrelationship drop foreign key service_advisor_phone_id_refs_id_ff3268c1;


alter table gladminds_coupondata  add foreign key (sa_phone_number_id) references aftersell_serviceadvisor(id);
show create table gladminds_coupondata;
alter table gladminds_coupondata drop foreign key sa_phone_number_id_refs_id_add685cd;
drop table gladminds_serviceadvisor;

#################################################################
alter table gladminds_coupondata add servicing_dealer_id integer, add constraint foreign key (servicing_dealer_id) references aftersell_registereddealer(id);
alter table gladminds_serviceadvisorcouponrelationship add dealer_id_id integer, add constraint foreign key (dealer_id_id) references aftersell_registereddealer(id);

alter table gladminds_customertempregistration add remarks VARCHAR(500) null;
alter table gladminds_customertempregistration add tagged_sap_id VARCHAR(215) null;


alter table  gladminds_productdata add veh_reg_no VARCHAR(15) null;
alter table gladminds_gladmindusers add pincode VARCHAR(15) null;