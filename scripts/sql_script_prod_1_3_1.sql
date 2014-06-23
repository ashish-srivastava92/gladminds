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
