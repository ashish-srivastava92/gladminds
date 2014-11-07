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

cur.execute("SELECT * FROM gladminds_productdata limit 100")
product_data = cur.fetchall()


def process_query(data):
    print "products", data.get('vin')
    print "----------------------------------"
# print "length",  len(products)
	try:
		cur2.execute("INSERT INTO bajaj_productdata (id, vin, sap_customer_id, product_purchase_date, invoice_date, engine,                  			customer_product_number, purchased_from, seller_email, seller_phone, warranty_yrs, insurance_yrs, invoice_loc, 						     warranty_loc,insurance_loc, last_modified, created_on , isActive,veh_reg_no,customer_phone_number_id,product_type_id, 			dealer_id_id) VALUES (%s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(data.get('id'), data.get('vin'),data.get('sap_customer_id'),data.get('product_purchase_date'),data.get('invoice_date'),data.get('engine'),data.get('customer_product_number'), data.get('purchased_from'), data.get('seller_email'), data.get('seller_phone'), data.get('warranty_yrs'), data.get('insurance_yrs'), data.get('invoice_loc'), data.get('warranty_loc'), data.get('insurance_loc'), data.get('last_modified'), data.get('created_on '), data.get('isActive'),data.get('veh_reg_no'), data.get(' customer_phone_number_id'), data.get('product_type_id'),data.get('dealer_id_id')))
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
	temp['sap_customer_id'] = data[4]
	temp['product_purchase_date'] = data[5]
	temp['invoice_date'] = data[6]
	temp['engine'] = data[0]
	temp['customer_product_number'] = data[8]
	temp['purchased_from'] = data[9]
	temp['seller_email'] = data[10]
	temp['seller_phone'] = data[11]
	temp['warranty_yrs'] = data[12]
	temp['insurance_yrs'] = data[13]
	temp['insurance_yrs'] = data[14]
	temp['invoice_loc'] = data[15]
	temp['warranty_loc'] = data[16]
	temp['insurance_loc'] = data[17]
	temp['last_modified'] = data[18]
	temp['created_on'] = data[19]
	temp['isActive'] = data[20]
	temp['veh_reg_no'] = data[21]
	temp['order'] = data[22]
	temp['customer_phone_number_id'] = data[2]
	temp['product_type_id'] = data[3]
	temp['dealer_id_id'] = data[7]
	products.append(temp)
pool.map(process_query, products)
end_time = time.time()
#print "..........Total TIME.........", end_time-start_time

