alter table gladminds_gladmindusers add column accepted_terms bool default 0;
alter table gladminds_gladmindusers add column pincode varchar(15) null;
alter table gladminds_gladmindusers add column tshirt_size VARCHAR(6) NULL CHECK (tshirt_size IN ('S', 'M', 'L', 'XL'));
alter table gladminds_gladmindusers drop gender;
alter table gladminds_gladmindusers add column gender VARCHAR(6) NULL CHECK (gender IN ('M', 'F', 'X'));
alter table gladminds_producttypedata add warranty_email VARCHAR(215);
alter table gladminds_producttypedata add warranty_phone VARCHAR(15);
alter table aftersell_feedback add column closed_date datetime;
ALTER TABLE aftersell_feedback ADD assign_to_reporter boolean default false; 
