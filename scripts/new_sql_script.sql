alter table gm_containertracker add column shippingline_id varchar(50) null;
alter table gm_containertracker add column ib_dispatch_dt int null;
alter table gm_containertracker add column no_of_containers int null;
alter table gm_containertracker add column cts_created_date  datetime  null;
alter table gm_containertracker modify container_no varchar(50) null;
alter table gm_containertracker modify seal_no varchar(50) null;
alter table gm_containertracker add column submitted_by varchar(50) null;

alter table gm_containertracker drop column ib_dispatch_dt ;
alter table gm_containertracker add column ib_dispatch_dt datetime null;

For epc
IN bajaj db; 
update gm_bomplate set plate_image = concat("qa/bajaj/plates/", plate_id, ".png") ;
update gm_bomplate set plate_image_with_part = concat("qa/bajaj/plates_with_part/", plate_id, ".png") ;

IN bajajcv and probiking
update gm_bomplate set plate_image = concat("qa/bajaj/plates/", plate_id, ".PNG") ;
update gm_bomplate set plate_image_with_part = concat("qa/bajaj/plates_with_part/", plate_id, ".PNG") ;

alter table gm_bomvisualization add column status varchar(25) null;
alter table gm_bomvisualization add column published_date datetime null;
alter table gm_bomvisualization add column remarks varchar(500) null;

alter table gm_userprofile add column reset_password boolean default false;
alter table gm_userprofile add column reset_date datetime null;
alter table gm_producttype add column overview varchar(512) null;

alter table gm_producttype add brand_id integer;
alter table gm_producttype add foreign key (brand_id) references gm_producttype(id);

alter table afterbuy_userproduct add column is_accepted boolean default false;  
alter table afterbuy_consumer add column is_phone_verified boolean default false;
alter table afterbuy_userproduct add column service_reminder int null;
alter table afterbuy_userproduct add column details_completed int null;
alter table afterbuy_userproduct add column manual_link varchar(512) null;
alter table afterbuy_producttype add column overview varchar(512) null;

alter table afterbuy_userproduct drop foreign key `brand_id_refs_id_e5504abf`;
alter table afterbuy_userproduct drop column brand_id;

alter table afterbuy_producttype add brand_id integer;
alter table afterbuy_producttype add foreign key (brand_id) references afterbuy_producttype(id);

alter table afterbuy_userproduct drop column nick_name;
alter table afterbuy_userproduct add column nick_name varchar(100) null;

alter table gm_manufacturingdata add column is_discrepant bool default 0;
alter table gm_manufacturingdata add column sent_to_sap bool default 0;

alter table gm_containerindent drop foreign key `transporter_id_refs_id_52bca095`;
alter table gm_containerindent drop column transporter_id;
alter table gm_containerlr add column transporter_id integer;
alter table gm_containerlr add foreign key (transporter_id) references gm_transporter(id);
update gm_containerlr new inner join gm_containertracker old on old.transaction_id=new.transaction_id set new.transporter_id=old.transporter_id;
alter table gm_containerlr add column partner_name varchar(50);

alter table gm_brandproductrange drop column vertical;

alter table gm_bomheader add column revision_number int default 0;