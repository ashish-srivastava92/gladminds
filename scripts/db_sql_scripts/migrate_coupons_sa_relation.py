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

CUR_OLD.execute("SELECT * FROM gladminds_serviceadvisorcouponrelationship")
COUPON_DATA = CUR_OLD.fetchall()

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

DB_OLD.close()
DB_NEW.close()
FILE = open('coupon_sa.out', 'a+')

def process_query(data):
    db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db="bajaj") # name of the data base

    cur_new = db_new.cursor()     
    try:
        today = datetime.now()        
        old_sa = OLD_SA_DATA[data.get('service_advisor_phone_id')]
        sa = SA_DATA[old_sa]
        
        cur_new.execute("INSERT INTO bajaj_serviceadvisorcouponrelationship (id, created_date, modified_date,\
        unique_service_coupon_id, service_advisor_id) VALUES\
        (%s, %s, %s, %s, %s)",(data.get('id'),today, today, data.get('unique_service_coupon_id'), sa))
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
        temp['unique_service_coupon_id'] = data[1]
        temp['service_advisor_phone_id'] = data[2]
        coupons.append(temp)
    POOL.map(process_query, coupons)

format_data(COUPON_DATA)
TOTAL_END_TIME = time.time()
FILE.write(str("..........Total TIME TAKEN......... {0}".format(TOTAL_END_TIME-TOTAL_START_TIME)) + '\n')
FILE.close()