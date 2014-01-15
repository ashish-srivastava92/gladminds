from django.db import models
from django.db import connection
from datetime import datetime
from gladminds.models import common
from gladminds import utils,  message_template as templates

tuple_to_str = lambda tup: str(tuple(tup)) if len(tup)>1 else "('"+str(tup[0])+"')"
def get_customers_to_send_reminder(*args, **kwargs):
    from gladminds.tasks import send_reminder_message
    REMINDER_QUERY = """SELECT gc.id, gu.phone_number, unique_service_coupon, product_id, expired_date, valid_days, valid_kms FROM gladminds_customerdata gc inner join gladminds_gladmindusers gu on gc.phone_number_id = gu.id  WHERE DATE(expired_date) = DATE_ADD(DATE(NOW()),INTERVAL 7 DAY) AND is_closed !=1 AND is_expired!=1 AND last_reminder_date is NULL;"""
    usc_list=[]
    cursor = connection.cursor()
    cursor.execute(REMINDER_QUERY)
    desc = cursor.description
    data_list = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
    for data in data_list:
        phone_number = data['phone_number']
        message = templates.REMINDER_COUPON_EXPIRY.format(data['unique_service_coupon'], data['product_id'], data['expired_date'])
        send_reminder_message.delay(phone_number = phone_number, message = message)
        usc_list.append(data['unique_service_coupon'])
    #After Sending all message into celery queue, update the schedule time in database
    if len(usc_list):
        usc_tup =  tuple_to_str(usc_list)
        UPDATE_CUSTOMER_DATA = """UPDATE gladminds_customerdata SET last_reminder_date = DATE(NOW()) WHERE unique_service_coupon IN {0};""".format(usc_tup)
        cursor.execute(UPDATE_CUSTOMER_DATA)
    
def get_customers_to_send_reminder_by_admin(*args, **kwargs):
    REMINDER_QUERY = """SELECT gc.id, gu.phone_number, unique_service_coupon, product_id, expired_date, valid_days, valid_kms FROM gladminds_customerdata gc inner join gladminds_gladmindusers gu on gc.phone_number_id = gu.id  WHERE DATE(expired_date) = DATE_ADD(DATE(NOW()),INTERVAL 31 DAY) AND is_closed !=1 AND is_expired!=1 AND last_reminder_date is NULL;"""
    cursor = connection.cursor()
    cursor.execute(REMINDER_QUERY)
    desc = cursor.description
    data_list = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
    for data in data_list:
        phone_number = data['phone_number']
        message = REMINDER_COUPON_EXPIRY.format(data['unique_service_coupon'], data['product_id'], data['expired_date'])
        send_reminder_message.delay(phone_number = phone_number, message = message)       

def import_data_from_sap(*args, **kwargs):
    pass