import MySQLdb
import time
import os
from multiprocessing.dummy import Pool
from datetime import datetime

TOTAL_START_TIME = time.time()
POOL = Pool(50)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'gladminds')
MIGRATE_DB = os.environ.get('MIGRATE_DB','gladmindsdb')


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

CUR_OLD.execute("SELECT * FROM gladminds_oldfscdata")
OLD_FSC_DATA = CUR_OLD.fetchall()

CUR_OLD.execute('select * from aftersell_registereddealer')
OLD_DEALERS = CUR_OLD.fetchall()
OLD_DEALER_DATA={}
for old_dealer in OLD_DEALERS:
    OLD_DEALER_DATA[old_dealer[0]]=old_dealer[1]

CUR_NEW.execute('select * from bajaj_dealer')
DEALERS = CUR_NEW.fetchall()
DEALER_DATA={}
for dealer in DEALERS:
    DEALER_DATA[dealer[2]]=dealer[3]

DB_OLD.close()
DB_NEW.close()
FILE = open('old_fsc.out', 'a+')

def process_query(data):
    db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                         user=DB_USER, # your username
                          passwd=DB_PASSWORD, # your password
                          db="bajaj") # name of the data base
    
    cur_new = db_new.cursor()
    try:
        today = datetime.now()
        old_dealer = OLD_DEALER_DATA[data.get('servicing_dealer_id')]
        dealer = DEALER_DATA[old_dealer]
        
        cur_new.execute("INSERT INTO bajaj_oldfscdata (id, created_date, modified_date,\
        unique_service_coupon, valid_days, valid_kms, service_type, status,\
        closed_date, mark_expired_on, actual_service_date, actual_kms, last_reminder_date,\
        schedule_reminder_date, extended_date, sent_to_sap,\
        credit_date, credit_note, special_case, missing_field, missing_value,\
        product_id, dealer_id) VALUES\
         (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
        %s, %s, %s, %s, %s, %s, %s, %s, %s)",(data.get('id'),today, today,\
        data.get('unique_service_coupon'), data.get('valid_days'),
        data.get('valid_kms'), data.get('service_type'), data.get('status'),
        data.get('closed_date'), data.get('mark_expired_on'), data.get('actual_service_date'),
        data.get('actual_kms'), data.get('last_reminder_date'), data.get('schedule_reminder_date'),
        data.get('extended_date'), data.get('sent_to_sap'), data.get('credit_date'),
        data.get('credit_note'),data.get('special_case'),data.get('missing_field'),
        data.get('missing_value'), data.get('vin_id'), dealer))
        db_new.commit()
    except Exception as ex:
        db_new.rollback()
        e='[Error]: {0} {1}'.format(data.get('id'), ex)
        FILE.write(str(e) + '\n')
    db_new.close()
    
 
def format_data(coupon_data):
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
        temp['missing_field'] = data[21]
        temp['missing_value'] = data[22]
        coupons.append(temp)
    POOL.map(process_query, coupons)

format_data(OLD_FSC_DATA)
TOTAL_END_TIME = time.time()
FILE.write(str("..........Total TIME TAKEN......... {0}".format(TOTAL_END_TIME-TOTAL_START_TIME)) + '\n')
FILE.close()