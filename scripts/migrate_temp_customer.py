import MySQLdb
import time
import os
from multiprocessing.dummy import Pool
from datetime import datetime

POOL = Pool(50)
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

CUR_OLD.execute("SELECT * FROM gladminds_customertempregistration")
CUST_DATA = CUR_OLD.fetchall()
DB_OLD.close()
FILE = open('temp_cust.out', 'a+')

def process_query(data):
    db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                         user=DB_USER, # your username
                          passwd=DB_PASSWORD, # your password
                          db="bajaj") # name of the data base
    
    cur_new = db_new.cursor()
    try:
        today = datetime.now()
        
        cur_new.execute("INSERT INTO bajaj_customertempregistration (id, created_date, modified_date,\
        new_customer_name, new_number, product_purchase_date, temp_customer_id, sent_to_sap,\
        remarks, tagged_sap_id, product_data_id) VALUES\
         (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(data.get('id'),today, today,\
        data.get('new_customer_name'), data.get('new_number'),
        data.get('product_purchase_date'), data.get('temp_customer_id'), data.get('sent_to_sap'),
        data.get('remarks'), data.get('tagged_sap_id'),data.get('product_data_id')))
        
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
        temp['product_data_id'] = data[1]
        temp['new_customer_name'] = data[2]
        temp['new_number'] = data[3]
        temp['product_purchase_date'] = data[4]
        temp['temp_customer_id'] = data[5]
        temp['sent_to_sap'] = data[6]
        temp['remarks'] = data[7]
        temp['tagged_sap_id'] = data[8]
        coupons.append(temp)
    POOL.map(process_query, coupons)

format_data(CUST_DATA)
TOTAL_END_TIME = time.time()
FILE.write(str("..........Total TIME TAKEN......... {0}".format(TOTAL_END_TIME-TOTAL_START_TIME)) + '\n')
FILE.close()
