alter table gladminds_gladmindusers add column accepted_terms bool default 0;
alter table gladminds_gladmindusers add column pincode varchar(15) null;
alter table gladminds_gladmindusers add column tshirt_size VARCHAR(6) NULL CHECK (tshirt_size IN ('S', 'M', 'L', 'XL'));
alter table gladminds_gladmindusers drop gender;
alter table gladminds_gladmindusers add column gender VARCHAR(6) NULL CHECK (gender IN ('M', 'F', 'X'));