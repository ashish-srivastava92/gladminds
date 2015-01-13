
update bajaj_coupondata c set c.valid_kms = (case when c.service_type=1 then 2000 when c.service_type=2 then 8000 when c.service_type=3 then 15000 end),c.valid_days = (case when c.service_type=1 then 365 when c.service_type=2 then 730 when c.service_type=3 then 730 end),c.status=1 where c.status not in (2, 6);

update bajaj_coupondata c join bajaj_productdata p on c.product_id=p.id set c.mark_expired_on = (select ADDDATE(p.purchase_date, (case when c.service_type=1 then 365 when c.service_type=2 then 730 when c.service_type=3 then 730 end )))  where c.status not in (2, 6) and p.purchase_date is not null;

update bajaj_coupondata c join bajaj_productdata p on c.product_id=p.id set c.extended_date = (select ADDDATE(p.purchase_date, (case when c.service_type=1 then 365 when c.service_type=2 then 730 when c.service_type=3 then 730 end )))  where c.status not in (2, 4, 6) and p.purchase_date is not null;

select count(*) from bajaj_coupondata where status not in (2,6) and service_type = 1 and (valid_kms!=2000 or valid_days!=365);

select count(*) from bajaj_coupondata where status not in (2,6) and service_type = 2 and (valid_kms!=8000 or valid_days!=730);

select count(*) from bajaj_coupondata where status not in (2,6) and service_type = 3 and (valid_kms!=15000 or valid_days!=730);


109304  service_type = 1 and (valid_kms!=2000 or valid_days!=365);
238386  service_type = 2 and (valid_kms!=8000 or valid_days!=730);
138791  service_type = 3 and (valid_kms!=15000 or valid_days!=730);
				
matched    affected
7585673		498834

1135304		29109
			
1135307	    29487
