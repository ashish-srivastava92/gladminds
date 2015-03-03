alter table bajaj_vinsyncfeedlog add ucn_count int(5) null;
alter table bajaj_feedback add file_location varchar (215) null;
update bajaj_smslog set action='RECEIVED' where action='RECIEVED';
alter table bajaj_customertempregistration add mobile_number_update_count int(5) null;
update bajaj_customertempregistration set mobile_number_update_count =0;
alter table bajaj_customertempregistration drop column mobile_number_update_count ;
alter table bajaj_customertempregistration add mobile_number_update_count int(5) default 0 ;
alter table bajaj_couponfact add column data_type varchar(20) null;

################################V0.1.5###############################################

alter table bajaj_customertempregistration add column email_flag boolean default False;
update bajaj_customertempregistration set email_flag = 1 where created_date <= '2015-01-06';

select a.asc_id, a.user_id, d.dealer_id, d.user_id from bajaj_authorizedservicecenter a inner join bajaj_dealer d on d.dealer_id=a.asc_id;
alter table bajaj_oldfscdata add column servicing_dealer varchar(50) null;
show create table bajaj_oldfscdata;
update bajaj_oldfscdata o set o.servicing_dealer=(select dealer_id from bajaj_dealer where d.user_id=o.dealer_id);
alter table bajaj_oldfscdata drop foreign key `dealer_id_refs_user_id_9e0dec6c`;
alter table bajaj_oldfscdata drop key `bajaj_oldfscdata_f65f7b5d`;
alter table bajaj_oldfscdata drop column dealer_id;
delete from bajaj_dealer where dealer_id in (select asc_id from bajaj_authorizedservicecenter);

#######################################V0.1.6##############################################################
alter table bajaj_authorizedservicecenter add asm_id integer;
alter table bajaj_authorizedservicecenter add foreign key (asm_id) references bajaj_areaservicemanager(id);
alter table bajaj_authorizedservicecenter add column asc_owner varchar(100) null;
alter table bajaj_customertempregistration add column update_history varchar(500) null;
alter table bajaj_authorizedservicecenter add column asc_owner_phone varchar(50) null;
alter table bajaj_authorizedservicecenter add column asc_owner_email varchar(100) null;


alter table bajaj_customertempregistration drop column old_number;
alter table bajaj_customertempregistration drop column update_history;
alter table bajaj_customerupdatehistory add email_flag boolean default False not null;
alter table bajaj_customertempregistration drop column email_flag;
alter table bajaj_vinsyncfeedlog add column sent_to_sap boolean default False;

alter table demo_feedback add sub_department_id integer;
alter table demo_feedback add foreign key (sub_department_id) references demo_departmentsubcategories(id);

alter table bajaj_feedback add sub_department_id integer;
alter table bajaj_feedback add foreign key (sub_department_id) references bajaj_departmentsubcategories(id);

alter table demo_servicedeskuser add sub_department_id integer;
alter table demo_servicedeskuser add foreign key (sub_department_id) references demo_departmentsubcategories(id);
alter table demo_userprofile add column department varchar(100) null;
alter table bajaj_userprofile add column department varchar(100) null;

alter table bajaj_dealer add column use_cdms boolean default True;
alter table demo_dealer add column use_cdms boolean default True;

alter table bajaj_productdata add constraint unique(engine);
alter table bajaj_productdata add column sku_code varchar(25) null;
