
###### small-numbers table
 DROP TABLE IF EXISTS numbers_small;
CREATE TABLE numbers_small (number INT);
INSERT INTO numbers_small VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);

###### main numbers table
 DROP TABLE IF EXISTS numbers;
CREATE TABLE numbers (number BIGINT);
INSERT INTO numbers
SELECT thousands.number * 1000 + hundreds.number * 100 + tens.number * 10 + ones.number
 FROM numbers_small thousands, numbers_small hundreds, numbers_small tens, numbers_small ones
LIMIT 1000000;

###### date table
DROP TABLE IF EXISTS bajaj_couponfact;
DROP TABLE IF EXISTS bajaj_datedimension;
CREATE TABLE bajaj_datedimension (
      date_id          BIGINT PRIMARY KEY, 
      date             DATE NOT NULL,
      timestamp        BIGINT NOT NULL,
      weekend          CHAR(10) NOT NULL DEFAULT "Weekday",
      day_of_week      CHAR(10) NOT NULL,
      month            CHAR(10) NOT NULL,
      month_day        INT NOT NULL, 
      year             INT NOT NULL,
      week_starting_monday CHAR(2) NOT NULL,
     UNIQUE KEY `date` (`date`),
     KEY `year_week` (`year`,`week_starting_monday`)
);

###### populate it with days
INSERT INTO bajaj_datedimension (date_id, date)
SELECT number, DATE_ADD( '2014-01-01', INTERVAL number DAY )
 FROM numbers
WHERE DATE_ADD( '2014-01-01', INTERVAL number DAY ) BETWEEN '2014-01-01' AND '2020-01-01'
ORDER BY number;

###### fill in other rows
UPDATE bajaj_datedimension SET
      timestamp=   UNIX_TIMESTAMP(date),
      day_of_week= DATE_FORMAT( date, "%W" ),
      weekend=     IF( DATE_FORMAT( date, "%W" ) IN ('Saturday','Sunday'), 'Weekend', 'Weekday'),
      month=       DATE_FORMAT( date, "%M"),
      year =       DATE_FORMAT( date, "%Y" ),
      month_day =  DATE_FORMAT( date, "%d" );

#########################################################################################

CREATE TABLE `bajaj_couponfact` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `closed` bigint NOT NULL,
    `inprogress` bigint NOT NULL,
    `expired` bigint NOT NULL,
    `unused` bigint NOT NULL,
    `exceeds` bigint NOT NULL,
    `data_type` varchar(20) NOT NULL,
    `date_id` bigint NOT NULL,
    UNIQUE (`date_id`, `data_type`)
)
;
ALTER TABLE `bajaj_couponfact` ADD CONSTRAINT `date_id_refs_date_id_016dde9e` FOREIGN KEY (`date_id`) REFERENCES `bajaj_datedimension` (`date_id`);

#######################################FILL IN FACT WITH MOCK################
insert into bajaj_couponfact(closed, inprogress, expired, unused, exceeds, data_type, date_id) select 0, 0, 0, 0, 0, 'TOTAL',date_id from bajaj_datedimension;


###################COUPON FACT TABLE UPDATE############################

UPDATE bajaj_couponfact b , (select stat.date, stat.count from (select d.date_id as date, count(*) as count from bajaj_coupondata b inner join bajaj_datedimension d on DATE(b.closed_date)=d.date group by DATE(closed_date)) as stat ) as stats set b.closed=stats.count where b.date_id=stats.date;

UPDATE bajaj_couponfact b , (select stat.date, stat.count from (select d.date_id as date, count(*) as count from bajaj_coupondata b inner join bajaj_datedimension d on DATE(b.actual_service_date)=d.date group by DATE(actual_service_date)) as stat ) as stats set b.inprogress=stats.count where b.date_id=stats.date;

set @csum := 0;
UPDATE bajaj_couponfact b , (select d.date_id as date, mid_stats.sum as sum from (select stat.date, (@csum := @csum + stat.count) as sum from (select DATE(created_date) as date,count(*) as count from bajaj_coupondata where DATE(created_date)=DATE(modified_date) and status=1 group by DATE(created_date)) as stat) as mid_stats inner join bajaj_datedimension d on d.date=mid_stats.date) as stats  set b.unused=stats.sum where b.date_id=stats.date

