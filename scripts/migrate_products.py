import MySQLdb
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from multiprocessing.dummy import Pool
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="hasher123", # your password
                      db="gladminds_qa") # name of the data base

db2 = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="hasher123", # your password
                      db="bajaj") # name of the data base



# you must create a Cursor object. It will let
cur = db.cursor() 
cur2 = db2.cursor()

cur.execute("SELECT p.*, d.dealer_id, c.customer_name, c.phone_number, \
             c.registration_date, t.product_type FROM gladminds_productdata as p, \
             aftersell_registereddealer as d, gladminds_gladmindusers as c,\
            gladminds_producttypedata as t where p.product_type_id=t.product_type_id\
            and p.dealer_id_id=d.id and p.customer_phone_number_id=c.id limit 1")
product_data = cur.fetchall()


def process_query(data):
    print "products", data.get('vin')
    print "----------------------------------"
    try:
        today = datetime.now()
        print "get the dealer", data.get('dealer_id')
        query1 = "select * from bajaj_dealer where dealer_id  = %(dealer_id)s"
        cur_new.execute(query1, {'dealer_id': data.get('dealer_id')})
        dealer = cur_new.fetchone()
        print "--------------- fetched associated dealer", dealer
        
        print "get the product type", data.get('product_type')
        query2 = "select * from bajaj_producttype where product_type  = %(product_type)s"
        cur_new.execute(query2, {'product_type': data.get('product_type')})
        product_type = cur_new.fetchone()
        print "--------------- fetched associated product type", product_type
        
        
        cur2.execute("INSERT INTO bajaj_productdata (id, created_date, modified_date, product_id,\
             customer_id, purchase_date, invoice_date, engine, veh_reg_no, is_active,\
             customer_details_id, product_type_id, dealer_id_id) VALUES (%s, %s, %s, \
             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(data.get('id'),data.get('created_on'),
                    data.get('last_modified'), data.get('vin'), data.get('sap_customer_id'),
                    data.get('product_purchase_date'), data.get('invoice_date'),
                    data.get('engine'), data.get('veh_reg_no'), data.get('isActive'),
                    data.get('customer_phone_number_id'), dealer, product_type))
        
        db2.commit()
    except Exception as ex:
        print ex
 

import time
start_time = time.time()
pool = Pool(1)
count = 0

products = []
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
    temp['customer_name'] = data[24]
    temp['phone_number'] = data[25]
    temp['registration_date'] = data[26]
    temp['product_type'] = data[27]
    products.append(temp)
pool.map(process_query, products)
end_time = time.time()
#print "..........Total TIME.........", end_time-start_time
