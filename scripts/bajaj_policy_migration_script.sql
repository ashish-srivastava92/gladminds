
update bajaj_coupondata c set c.valid_kms = (case when c.service_type=1 then 2000 when c.service_type=2 then 8000 when c.service_type=3 then 15000 end),c.valid_days = (case when c.service_type=1 then 365 when c.service_type=2 then 730 when c.service_type=3 then 730 end),c.status=1 where c.status not in (2, 6);

update bajaj_coupondata c join bajaj_productdata p on c.product_id=p.id set c.mark_expired_on = (select ADDDATE(p.purchase_date, (case when c.service_type=1 then 365 when c.service_type=2 then 730 when c.service_type=3 then 730 end )))  where c.status not in (2, 6) and p.purchase_date is not null;

update bajaj_coupondata c join bajaj_productdata p on c.product_id=p.id set c.extended_date = (select ADDDATE(p.purchase_date, (case when c.service_type=1 then 365 when c.service_type=2 then 730 when c.service_type=3 then 730 end )))  where c.status not in (2, 4, 6) and p.purchase_date is not null;

select count(*) from bajaj_coupondata where status not in (2,6) and service_type = 1 and (valid_kms!=2000 or valid_days!=365);

select count(*) from bajaj_coupondata where status not in (2,6) and service_type = 2 and (valid_kms!=8000 or valid_days!=730);

select count(*) from bajaj_coupondata where status not in (2,6) and service_type = 3 and (valid_kms!=15000 or valid_days!=730);



select d2.user_id as prefix_id ,d2.dealer_id as prefix_did, d.dealer_id, d.user_id from bajaj_dealer as d, bajaj_dealer as d2 where d2.dealer_id like concat('00000',d.dealer_id);

update bajaj_coupondata c inner join (select d2.dealer_id as old_id , d.dealer_id as new_id from bajaj_dealer as d, bajaj_dealer as d2 where d2.dealer_id like concat('00000',d.dealer_id)) a on c.servicing_dealer = a.old_id set c.servicing_dealer=a.new_id;

update bajaj_oldfscdata c inner join (select d2.dealer_id as old_id , d.dealer_id as new_id from bajaj_dealer as d, bajaj_dealer as d2 where d2.dealer_id like concat('00000',d.dealer_id)) a on c.servicing_dealer_id = a.old_id set c.servicing_dealer_id=a.new_id;

select servicing_dealer from bajaj_coupondata c inner join (select d2.dealer_id as old_id , d.dealer_id as new_id from bajaj_dealer as d, bajaj_dealer as d2 where d2.dealer_id like concat('00000',d.dealer_id)) a on c.servicing_dealer = a.old_id;

select servicing_dealer from bajaj_oldfscdata c inner join (select d2.dealer_id as old_id , d.dealer_id as new_id from bajaj_dealer as d, bajaj_dealer as d2 where d2.dealer_id like concat('00000',d.dealer_id)) a on c.servicing_dealer = a.old_id;
