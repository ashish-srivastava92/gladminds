import MySQLdb
import time
import os
from multiprocessing.dummy import Pool
from datetime import datetime

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

db_old = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db="gladminds") # name of the data base

cur_old = db_old.cursor() 

db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db="bajaj") # name of the data base

cur_new = db_new.cursor() 

cur_old.execute("SELECT c.*, p.vin FROM gladminds_customertempregistration as c, gladminds_productdata as p \
               where c.product_data_id=p.id and c.product_data_id in (101964, 102344, 102664, 103889)")
coupon_data = cur_old.fetchall()


def process_query(data):
    print "--------------------coupons--------------", data.get('unique_service_coupon)')
    try:
        today = datetime.now()
        print "get the product", data.get('vin')
        query1 = "select * from bajaj_productdata where product_id  = %(product_id)s"
        cur_new.execute(query1, {'product_id': data.get('vin')})
        product = cur_new.fetchone()
        print "--------------- fetched associated product------------------------", product
        
        cur_new.execute("INSERT INTO bajaj_customertempregistration (id, created_date, modified_date,\
        new_customer_name, new_number, product_purchase_date, temp_customer_id, sent_to_sap,\
        remarks, tagged_sap_id, product_data_id) VALUES\
         (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(data.get('id'),today, today,\
        data.get('new_customer_name'), data.get('new_number'),
        data.get('product_purchase_date'), data.get('temp_customer_id'), data.get('sent_to_sap'),
        data.get('remarks'), data.get('tagged_sap_id'),product[0]))
        
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
        temp['product_data_id'] = data[1]
        temp['new_customer_name'] = data[2]
        temp['new_number'] = data[3]
        temp['product_purchase_date'] = data[4]
        temp['temp_customer_id'] = data[5]
        temp['sent_to_sap'] = data[6]
        temp['remarks'] = data[7]
        temp['tagged_sap_id'] = data[8]
        temp['vin'] = data[9]
        coupons.append(temp)
    pool.map(process_query, coupons)
    end_time = time.time()

format_data(coupon_data)

''' To migrate UCN RECOVERY DATA'''

cur_old.execute("SELECT c.*, a.username FROM aftersell_ucnrecovery as u, auth_user as a where u.user_id=a.id")
ucnrecover_data = cur_old.fetchall()

def process_query_ucnrecover(data):
    print "--------------------coupons--------------", data.get('unique_service_coupon')
    try:
        today = datetime.now()
        print "-------------- dealer", data.get('username')
        query = "select id from auth_user where username  = %(username)s"
        cur_new.execute(query, {'username': data.get('username')})
        dealer = cur_new.fetchall()[0]
        print "fetched dealer", dealer
        
        query2 = "select * from bajaj_userprofile where user_id  = %(user_id)s"
        cur_new.execute(query2, {'user_id': dealer[0]})
        dealer_pro = cur_new.fetchall()[0]
        print "fetched dealer profile", dealer_pro
        
        cur_new.execute("INSERT INTO bajaj_ucnrecovery (id, created_date, modified_date,\
        reason, customer_id, file_location, unique_service_coupon, user_id) VALUES\
         (%s, %s, %s, %s, %s, %s, %s, %s)",(data.get('id'),today, today,\
        data.get('reason'), data.get('customer_id'),
        data.get('file_location'), data.get('unique_service_coupon'), dealer_pro[11]))
        
        db_new.commit()        
        print "---------------DONE--------------------"
    except Exception as ex:
        db_new.rollback()
        print "----------------------SOMETHING WENT WRONG--------------------", ex
    
 
def format_data_ucnrecover(ucnrecover_data):
    start_time = time.time()
    pool = Pool(1)
    ucnrecovers=[]
    for data in ucnrecover_data:
        print "----------------", data
        temp = {}
        temp['id'] = data[0]
        temp['reason'] = data[1]
        temp['user_id'] = data[2]
        temp['sap_customer_id'] = data[3]
        temp['file_location'] = data[4]
        temp['request_date'] = data[5]
        temp['unique_service_coupon'] = data[6]
        temp['username'] = data[7]
        ucnrecovers.append(temp)
        print "------------------------", temp
    print "------------------", ucnrecovers
    pool.map(process_query_ucnrecover, ucnrecovers)
    end_time = time.time()

format_data_ucnrecover(ucnrecover_data)
