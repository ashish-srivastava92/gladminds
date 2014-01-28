from django.db import models
from django.db import connection
from datetime import datetime
from gladminds.models import common
from gladminds import utils,  message_template as templates

tuple_to_str = lambda tup: str(tuple(tup)) if len(tup)>1 else "('"+str(tup[0])+"')"
def get_customers_to_send_reminder(*args, **kwargs):
    from gladminds.tasks import send_reminder_message
    reminder_day = kwargs.get('reminder_day', None)
    REMINDER_QUERY = """SELECT gc.id, ggu.phone_number, gc.unique_service_coupon, gu.vin, DATE_FORMAT(gc.mark_expired_on, '%D %M %Y') as mark_expired_on, gc.valid_days, gc.valid_kms FROM gladminds_coupondata gc inner join gladminds_productdata gu on gc.vin_id = gu.id inner join gladminds_gladmindusers ggu on ggu.id = gu.customer_phone_number_id  WHERE DATE(mark_expired_on) = DATE_ADD(DATE(NOW()),INTERVAL {0} DAY) AND status !=2 AND status!=3 AND last_reminder_date is NULL;""".format(reminder_day)
    usc_list=[]
    cursor = connection.cursor()
    cursor.execute(REMINDER_QUERY)
    desc = cursor.description
    data_list = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
    for data in data_list:
        phone_number = data['phone_number']
        message = templates.get_template('SEND_CUSTOMER_COUPON_REMINDER').format(data['unique_service_coupon'], data['vin'], data['mark_expired_on'])
        send_reminder_message.delay(phone_number = phone_number, message = message)
        usc_list.append(data['unique_service_coupon'])
    
    #After Sending all message into celery queue, update the schedule time in database
    if len(usc_list):
        usc_tup =  tuple_to_str(usc_list)
        UPDATE_CUSTOMER_DATA = """UPDATE gladminds_coupondata SET DATE(last_reminder_date) = DATE(NOW()) WHERE unique_service_coupon IN {0};""".format(usc_tup)
        cursor.execute(UPDATE_CUSTOMER_DATA)
    
def get_customers_to_send_reminder_by_admin(*args, **kwargs):
    from gladminds.tasks import send_reminder_message
    SCHEDULE_REMINDER_QUERY = """SELECT gc.id, ggu.phone_number, gc.unique_service_coupon, gu.vin, DATE_FORMAT(gc.mark_expired_on, '%D %M %Y') as mark_expired_on, gc.valid_days, gc.valid_kms FROM gladminds_coupondata gc inner join gladminds_productdata gu on gc.vin_id = gu.id inner join gladminds_gladmindusers ggu on ggu.id = gu.customer_phone_number_id  WHERE status !=2 AND status!=3 AND DATE(schedule_reminder_date) = DATE(NOW());"""
    usc_list=[]
    cursor = connection.cursor()
    cursor.execute(SCHEDULE_REMINDER_QUERY)
    desc = cursor.description
    data_list = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
    for data in data_list:
        phone_number = data['phone_number']
        message = templates.get_template('SEND_CUSTOMER_COUPON_REMINDER').format(data['unique_service_coupon'], data['vin'], data['mark_expired_on'])
        send_reminder_message.delay(phone_number = phone_number, message = message)       
        usc_list.append(data['unique_service_coupon'])
    
    #After Sending all message into celery queue, update the schedule time in database
    if len(usc_list):
        usc_tup =  tuple_to_str(usc_list)
        UPDATE_CUSTOMER_DATA = """UPDATE gladminds_coupondata SET last_reminder_date = NOW(), schedule_reminder_date=NULL WHERE unique_service_coupon IN {0};""".format(usc_tup)
        cursor.execute(UPDATE_CUSTOMER_DATA)

def expire_service_coupon(*args, **kwargs):
    UPDATE_EXPIRE_STATUS_FOR_SERVICE_COUPON = """UPDATE gladminds_coupondata SET status=3 where mark_expired_on<NOW()"""
    try:
        cursor = connection.cursor()
        cursor.execute(UPDATE_EXPIRE_STATUS_FOR_SERVICE_COUPON)
    except Exception as ex:
        print "Caught exception : {0}".format(ex)

def import_data_from_sap(*args, **kwargs):
    pass