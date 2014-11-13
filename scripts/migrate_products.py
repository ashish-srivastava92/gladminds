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

cur_old.execute("SELECT p.*, d.dealer_id, t.product_type FROM gladminds_productdata as p, \
             aftersell_registereddealer as d, gladminds_producttypedata as t \
             where p.product_type_id=t.product_type_id\
            and p.dealer_id_id=d.id and p.id in (101964, 102344, 102664, 103889) limit 1000")
product_data = cur_old.fetchall()


def process_query(data):
    print "--------------------products--------------", data.get('vin')
    try:
        print "get the dealer", data.get('dealer_id')
        query1 = "select * from bajaj_dealer where dealer_id  = %(dealer_id)s"
        cur_new.execute(query1, {'dealer_id': data.get('dealer_id')})
        dealer = cur_new.fetchone()
        print "--------------- fetched associated dealer------------------------", dealer
        
        print "get the product type", data.get('product_type')
        query2 = "select * from bajaj_producttype where product_type  = %(product_type)s"
        cur_new.execute(query2, {'product_type': data.get('product_type')})
        product_type = cur_new.fetchone()
        print "--------------- fetched associated product type----------------", product_type
        
        customer_number=customer_name=customer_address=None
        if data.get('customer_phone_number_id'):
            print "get the customer", data.get('customer_phone_number_id')
            query3 = "select * from gladminds_gladmindusers where id  = %(id)s"
            cur_old.execute(query3, {'id': data.get('customer_phone_number_id')})
            customer = cur_old.fetchone()
            customer_name=customer[3]
            customer_number=customer[5]
            if customer[7]:
                customer_address=customer[7]+',' 
            if customer[9]:
                customer_address= customer_address + customer[9]+','
            if customer[14]:
                customer_address= customer_address + customer[14]
            print "--------------- fetched associated customer----------------", customer
        
        print "-----------Customer details------", customer_number, customer_name, customer_address
            
        cur_new.execute("INSERT INTO bajaj_productdata (id, created_date, modified_date, \
        product_id, customer_id, customer_phone_number, customer_name, customer_address,\
        purchase_date, invoice_date, engine, veh_reg_no, is_active,\
        product_type_id, dealer_id_id ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
        %s)",(data.get('id'),data.get('created_on'),
        data.get('last_modified'), data.get('vin'), data.get('sap_customer_id'),
        customer_number, customer_name, customer_address,
        data.get('product_purchase_date'), data.get('invoice_date'),
        data.get('engine'), data.get('veh_reg_no'), data.get('isActive'),
        product_type[2], dealer[3]))
        
        db_new.commit()
        print "---------------DONE--------------------"
    except Exception as ex:
        db_new.rollback()
        print "----------------------SOMETHING WENT WRONG--------------------", ex

def format_data(product_data):
    start_time = time.time()
    pool = Pool(1)
    products=[]
    for data in product_data:
        temp = {}
        temp['id'] = data[0]
        temp['vin'] = data[1]
        temp['customer_phone_number_id'] = data[2]
        temp['product_type_id'] = data[3]
        temp['sap_customer_id'] = data[4]
        
        temp['product_purchase_date'] = data[5]
        temp['invoice_date'] = data[6]
        temp['dealer_id_id'] = data[7]
        temp['engine'] = data[8]
        
        temp['customer_product_number'] = data[9]
        temp['purchased_from'] = data[10]
        temp['seller_email'] = data[11]
        temp['seller_phone'] = data[12]
        
        temp['warranty_yrs'] = data[13]
        temp['insurance_yrs'] = data[14]
        temp['invoice_loc'] = data[15]
        temp['warranty_loc'] = data[16]
        
        temp['insurance_loc'] = data[17]
        temp['last_modified'] = data[18]
        temp['created_on'] = data[19]
        temp['isActive'] = data[20]
        
        temp['order'] = data[21]
        temp['veh_reg_no'] = data[22]
        
        temp['dealer_id'] = data[23]
        temp['product_type'] = data[24]
        products.append(temp)
    pool.map(process_query, products)
    end_time = time.time()
#print "..........Total TIME.........", end_time-start_time
