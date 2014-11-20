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

DB_NEW = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                         user=DB_USER, # your username
                          passwd=DB_PASSWORD, # your password
                          db="bajaj") # name of the data base

CUR_NEW = DB_NEW.cursor()

CUR_OLD.execute('select * from aftersell_registereddealer where role="dealer"')
OLD_DEALERS = CUR_OLD.fetchall()
OLD_DEALER_DATA={}
for old_dealer in OLD_DEALERS:
    OLD_DEALER_DATA[old_dealer[0]]=old_dealer[1]
    
CUR_OLD.execute('select * from gladminds_producttypedata')
OLD_PRODUCTS = CUR_OLD.fetchall()
OLD_PRODUCTS_DATA={}
for old_product in OLD_PRODUCTS:
    OLD_PRODUCTS_DATA[old_product[0]]=old_product[3]

CUR_NEW.execute('select * from bajaj_dealer')
DEALERS = CUR_NEW.fetchall()
DEALER_DATA={}
for dealer in DEALERS:
    DEALER_DATA[dealer[2]]=dealer[3]
    
CUR_NEW.execute('select * from bajaj_producttype')
PRODUCTS = CUR_NEW.fetchall()
PRODUCTS_DATA={}
for product in PRODUCTS:
    PRODUCTS_DATA[product[3]]=product[0]

DB_NEW.close()

def process_query(data):
    
    db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                         user=DB_USER, # your username
                          passwd=DB_PASSWORD, # your password
                          db="bajaj") # name of the data base
    
    cur_new = db_new.cursor()
    try:
                
        old_dealer = OLD_DEALER_DATA[data.get('dealer_id_id')]
        dealer = DEALER_DATA[old_dealer]
        
        old_product_type = OLD_PRODUCTS_DATA[data.get('product_type_id')]
        product_type = PRODUCTS_DATA[old_product_type]
        
        customer_number=customer_name=customer_address=None
        if data.get('customer_phone_number_id'):
            db_old = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db=MIGRATE_DB) # name of the data base
            cur_old = db_old.cursor()
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
            db_old.close()
        
        cur_new.execute("INSERT INTO bajaj_productdata (id, created_date, modified_date, \
        product_id, customer_id, customer_phone_number, customer_name, customer_address,\
        purchase_date, invoice_date, engine, veh_reg_no, is_active,\
        product_type_id, dealer_id_id ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
        %s)",(data.get('id'),data.get('created_on'),
        data.get('last_modified'), data.get('vin'), data.get('sap_customer_id'),
        customer_number, customer_name, customer_address,
        data.get('product_purchase_date'), data.get('invoice_date'),
        data.get('engine'), data.get('veh_reg_no'), data.get('isActive'),
        product_type, dealer))
        db_new.commit()
    except Exception as ex:
        e='[Error]: {0} {1}'.format(data.get('vin'), ex)

        db_new.rollback()
        if 'Duplicate entry' not in e:
            print e
    db_new.close()

def format_data(product_data):
    
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
        
        products.append(temp)
    POOL.map(process_query, products)

def get_data(offset=0):
    print "OFFSET:", offset
    db_old = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db=MIGRATE_DB) # name of the data base

    cur_old = db_old.cursor()

    query= "SELECT * FROM gladminds_productdata limit 10000 offset %(offset)s"
    cur_old.execute(query, {'offset': offset})
    product_data = cur_old.fetchall()
    format_data(product_data)
    db_old.close()

CUR_OLD.execute('select count(*) from gladminds_productdata;')
DATA_COUNT = CUR_OLD.fetchone()[0]
DB_OLD.close()
while OFFSET<=DATA_COUNT:
    get_data(offset=OFFSET)
    OFFSET=OFFSET+10000
TOTAL_END_TIME = time.time()
print "..........Total TIME TAKEN.........", TOTAL_END_TIME-TOTAL_START_TIME