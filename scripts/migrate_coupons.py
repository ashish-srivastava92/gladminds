import MySQLdb
import time
import os
from multiprocessing.dummy import Pool
from datetime import datetime

POOL = Pool(100)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'gladminds')
MIGRATE_DB = os.environ.get('MIGRATE_DB','gladmindsdb')
OFFSET = int(os.environ.get('OFFSET',0))
TOTAL_START_TIME = time.time()


DB_OLD = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db=MIGRATE_DB) # name of the data base

CUR_OLD = DB_OLD.cursor()

DB_NEW = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                         user=DB_USER, # your username
                          passwd=DB_PASSWORD, # your password
                          db="bajaj") # name of the data base

CUR_NEW = DB_NEW.cursor()

CUR_OLD.execute('select * from aftersell_serviceadvisor')
OLD_SA = CUR_OLD.fetchall()
OLD_SA_DATA={}
for old_sa in OLD_SA:
    OLD_SA_DATA[old_sa[0]]=old_sa[1]

CUR_NEW.execute('select * from bajaj_serviceadvisor')
SA = CUR_NEW.fetchall()
SA_DATA={}
for sa in SA:
    SA_DATA[sa[2]]=sa[4]

DB_NEW.close()

def process_query(data):
    db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                         user=DB_USER, # your username
                          passwd=DB_PASSWORD, # your password
                          db="bajaj") # name of the data base
    cur_new = db_new.cursor()
    try:
        sa=None
        today = datetime.now()
        if data.get('sa_phone_number_id'):
            old_sa = OLD_SA_DATA[data.get('sa_phone_number_id')]
            sa = SA_DATA[old_sa]
        
        cur_new.execute("INSERT INTO bajaj_coupondata (id, created_date, modified_date,\
        unique_service_coupon, valid_days, valid_kms, service_type, status,\
        closed_date, mark_expired_on, actual_service_date, actual_kms, last_reminder_date,\
        schedule_reminder_date, extended_date, sent_to_sap,\
        credit_date, credit_note, special_case, product_id, service_advisor_id) VALUES\
         (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
        %s, %s, %s, %s, %s, %s, %s)",(data.get('id'),today, today,\
        data.get('unique_service_coupon'), data.get('valid_days'),
        data.get('valid_kms'), data.get('service_type'), data.get('status'),
        data.get('closed_date'), data.get('mark_expired_on'), data.get('actual_service_date'),
        data.get('actual_kms'), data.get('last_reminder_date'), data.get('schedule_reminder_date'),
        data.get('extended_date'), data.get('sent_to_sap'), data.get('credit_date'),
        data.get('credit_note'),data.get('special_case'),data.get('vin_id'), sa))
        
        db_new.commit()
    except Exception as ex:
        e='[Error]: {0} {1}'.format( data.get('vin'), ex)
        db_new.rollback()
        if 'Duplicate entry' not in e:
            print e
    db_new.close()
    
 
def format_data(coupon_data):
    pool = Pool(50)
    coupons=[]
    for data in coupon_data:
        temp = {}
        temp['id'] = data[0]
        temp['vin_id'] = data[1]
        temp['unique_service_coupon'] = data[2]
        temp['valid_days'] = data[3]
        temp['valid_kms'] = data[4]
        temp['service_type'] = data[5]
        temp['sa_phone_number_id'] = data[6]
        temp['status'] = data[7]
        temp['closed_date'] = data[8]
        temp['mark_expired_on'] = data[9]
        temp['actual_service_date'] = data[10]
        temp['actual_kms'] = data[11]
        temp['last_reminder_date'] = data[12]
        temp['schedule_reminder_date'] = data[13]
        temp['order'] = data[14]
        temp['extended_date'] = data[15]
        temp['servicing_dealer_id'] = data[16]
        temp['sent_to_sap'] = data[17]
        temp['credit_date'] = data[18]
        temp['credit_note'] = data[19]
        temp['special_case'] = data[20]
        
        coupons.append(temp)
    POOL.map(process_query, coupons)


def get_data(offset=0):
    print "OFFSET:", offset
    db_old = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db=MIGRATE_DB) # name of the data base

    cur_old = db_old.cursor()

    query= "SELECT * FROM gladminds_coupondata limit 1000 offset %(offset)s"
    cur_old.execute(query, {'offset': offset})
    product_data = cur_old.fetchall()
    format_data(product_data)
    db_old.close()

CUR_OLD.execute('select count(*) from gladminds_coupondata;')
DATA_COUNT = CUR_OLD.fetchone()[0]
DB_OLD.close()

while OFFSET<=DATA_COUNT:
    get_data(offset=OFFSET)
    OFFSET=OFFSET+1000
TOTAL_END_TIME = time.time()
print "..........Total TIME TAKEN.........", TOTAL_END_TIME-TOTAL_START_TIME