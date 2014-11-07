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

cur.execute("SELECT * FROM gladminds_coupondata limit 1")
coupon_data = cur.fetchall()


def process_query(data):
    print "coupon", data.get('id')
    print "----------------------------------"
# print "length",  len(products)
#    cur2.execute("INSERT INTO bajaj_productdata (id, vin, sap_customer_id, product_purchase_date, invoice_date, engine,                  customer_product_number, purchased_from, seller_email, seller_phone, warranty_yrs, insurance_yrs, invoice_loc, warranty_loc, insurance_loc, last_modified, created_on , isActive,veh_reg_no, customer_phone_number_id, product_type_id, dealer_id_id) VALUES (%s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(data.get('id'), data.get('vin'),data.get('sap_customer_id'),data.get('product_purchase_date'),data.get('invoice_date'),data.get('engine'),data.get('customer_product_number'), data.get('purchased_from'), data.get('seller_email'), data.get('seller_phone'), data.get('warranty_yrs'), data.get('insurance_yrs'), data.get('invoice_loc'), data.get('warranty_loc'), data.get('insurance_loc'), data.get('last_modified'), data.get('created_on '), data.get('isActive'),data.get('veh_reg_no'), data.get(' customer_phone_number_id'), data.get('product_type_id'),data.get('dealer_id_id')))
    db2.commit()


import time
start_time = time.time()
pool = Pool(1)
count = 0

coupons = []
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
	temp['seller_phone'] = data[9]
	temp['mark_expired_on'] = data[10]
	temp['actual_service_date'] = data[11]
	temp['actual_kms'] = data[12]
	temp['last_reminder_date'] = data[13]
	temp['schedule_reminder_date'] = data[14]
	temp['order'] = data[15]
	temp['extended_date'] = data[16]
	temp['servicing_dealer_id'] = data[17]
	temp['sent_to_sap'] = data[18]
	temp['credit_date'] = data[19]
	temp['credit_note'] = data[20]
	temp['special_case'] = data[21]
	coupons.append(temp)

pool.map(process_query, coupons)
print coupons
end_time = time.time()
#print "..........Total TIME.........", end_time-start_time

