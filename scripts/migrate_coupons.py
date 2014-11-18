import MySQLdb
import time
import os
from multiprocessing.dummy import Pool
from datetime import datetime

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

MIGRATE_DB = os.environ.get('MIGRATE_DB','gladminds')
db_old = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db=MIGRATE_DB) # name of the data base

cur_old = db_old.cursor() 

db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db="bajaj") # name of the data base

cur_new = db_new.cursor() 

def process_query(data):
    print "--------------------coupons--------------", data.get('vin_id)'), data.get('unique_service_coupon)')
    try:
        today = datetime.now()
        print "get the product", data.get('vin')
        query1 = "select * from bajaj_productdata where product_id  = %(product_id)s"
        cur_new.execute(query1, {'product_id': data.get('vin')})
        product = cur_new.fetchone()
        print "--------------- fetched associated product------------------------", product
        
        sa=None
        if data.get('sa_phone_number_id'):
            print "get the old sa", data.get('sa_phone_number_id')
            query2 = "select * from aftersell_serviceadvisor where id  = %(id)s"
            cur_old.execute(query2, {'id': data.get('sa_phone_number_id')})
            sa_old = cur_old.fetchone()
            print "--------------- fetched associated sa_old------------------------", sa_old
            
            print "get the new sa", sa_old[1]
            query3 = "select * from bajaj_serviceadvisor where service_advisor_id  = %(service_advisor_id)s"
            cur_new.execute(query3, {'service_advisor_id': sa_old[1]})
            sa_new = cur_new.fetchone()
            print "--------------- fetched associated SA----------------", sa_new
            sa=sa_new[4]
        
        print "---------------------sa------------------", sa    
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
        data.get('credit_note'),data.get('special_case'),product[0], sa))
        
        db_new.commit()
        print "---------------DONE--------------------"
    except Exception as ex:
        db_new.rollback()
        print "----------------------SOMETHING WENT WRONG--------------------", ex
    
 
def format_data(coupon_data):
    start_time = time.time()
    pool = Pool(1)
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
        temp['vin'] = data[21]
        coupons.append(temp)
    pool.map(process_query, coupons)
    end_time = time.time()
    print "..........TIME TAKEN.........", end_time-start_time


def get_data(offset=0):
    query= "SELECT c.*, p.vin FROM gladminds_coupondata as c, gladminds_productdata as p\
             where c.vin_id=p.id limit 10000 offset %(offset)s"
    cur_old.execute(query, {'offset': offset})
    coupon_data = cur_old.fetchall()
    format_data(coupon_data)

cur_old.execute('select count(*) from gladminds_coupondata;')
coupon_data_count = cur_old.fetchone()[0]
i=0
while i<=coupon_data_count:
    get_data(offset=i)
    i=i+1000
total_end_time = time.time()
print "..........Total TIME TAKEN.........", total_end_time-total_start_time