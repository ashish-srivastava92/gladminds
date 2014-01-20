from __future__ import absolute_import
from celery import shared_task
from django.conf import settings
from gladminds.utils import save_log
from gladminds.dao.smsclient import MockSmsClient
from gladminds import taskmanager
import logging
logger = logging.getLogger(__name__)

"""
This task send sms to customer on customer registration
"""
@shared_task
def send_registration_detail(*args, **kwargs):
    try:
        client = settings.SMS_CLIENT_DETAIL
        sms_client = MockSmsClient(**client)
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        logger.info(debug_message)
        kwargs = {
                    'action':'SENT',
                    'reciever': '55680',
                    'sender':str(phone_number),
                    'message': message,
                    'status':'success'
                  }
        save_log(**kwargs)
    except Exception as ex:
        send_registration_detail.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries = 5)
        
"""
This task send customer valid service detail
""" 
@shared_task
def send_service_detail(*args, **kwargs):
    try:
        client = settings.SMS_CLIENT_DETAIL
        sms_client = MockSmsClient(**client)
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        response_data = sms_client.send_stateless(**kwargs)
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        logger.info(debug_message)
        kwargs = {
                    'action':'SENT',
                    'reciever': '55680',
                    'sender':str(phone_number),
                    'message': message,
                    'status':'success'
                  }
        save_log(**kwargs)
    except Exception as ex:
        send_service_detail.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries = 5)

"""
This job send sms to service advisor, whether the coupon is valid or not 
"""
@shared_task
def send_coupon_validity_detail(*args, **kwargs):
    try:
        client = settings.SMS_CLIENT_DETAIL
        sms_client = MockSmsClient(**client)
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        logger.info(debug_message)
        kwargs = {
                    'action':'SENT',
                    'reciever': '55680',
                    'sender':str(phone_number),
                    'message': message,
                    'status':'success'
                  }
        save_log(**kwargs)
    except Exception as ex:
        send_registration_detail.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries = 5)



"""
This job send sms to customer when SA send 
 query, whether the coupon is valid or not 
"""
@shared_task
def send_coupon_detail_customer(*args, **kwargs):
    try:
        client = settings.SMS_CLIENT_DETAIL
        sms_client = MockSmsClient(**client)
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        logger.info(debug_message)
        kwargs = {
                    'action':'SENT',
                    'reciever': '55680',
                    'sender':'GCP',
                    'message': message,
                    'status':'success'
                  }
        save_log(**kwargs)
    except Exception as ex:
        send_registration_detail.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries = 5)




"""
This job send reminder sms to customer
"""
@shared_task
def send_reminder_message(*args, **kwargs):
    try:
        client = settings.SMS_CLIENT_DETAIL
        sms_client = MockSmsClient(**client)
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        logger.info(debug_message)
        kwargs = {
                    'action':'SENT Reminder',
                    'reciever': '55680',
                    'sender':str(phone_number),
                    'message': message,
                    'status':'success'
                  }
        save_log(**kwargs)
    except Exception as ex:
        send_reminder_message.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries = 5)




"""
This job send coupon close message
"""
@shared_task
def send_coupon_close_message(*args, **kwargs):
    try:
        client = settings.SMS_CLIENT_DETAIL
        sms_client = MockSmsClient(**client)
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        logger.info(debug_message)
        kwargs = {
                    'action':'SENT Reminder',
                    'reciever': '55680',
                    'sender':str(phone_number),
                    'message': message,
                    'status':'success'
                  }
        save_log(**kwargs)
    except Exception as ex:
        send_coupon_close_message.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries = 5)


"""
This job send coupon close message to customer
"""
@shared_task
def send_close_sms_customer(*args, **kwargs):
    try:
        client = settings.SMS_CLIENT_DETAIL
        sms_client = MockSmsClient(**client)
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        logger.info(debug_message)
        kwargs = {
                    'action':'SENT',
                    'reciever': '55680',
                    'sender':'GCS',
                    'message': message,
                    'status':'success'
                  }
        save_log(**kwargs)
    except Exception as ex:
        send_coupon_close_message_customer.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries = 5)

@shared_task
def send_brand_sms_customer(*args, **kwargs):
    try:
        client = settings.SMS_CLIENT_DETAIL
        sms_client = MockSmsClient(**client)
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        logger.info(debug_message)
        kwargs = {
                    'action':'SENT',
                    'reciever': '55680',
                    'sender':'GCS',
                    'message': message,
                    'status':'success'
                  }
        save_log(**kwargs)
    except Exception as ex:
        send_brand_sms_customer.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries = 5)





"""
Crontab to send reminder sms to customer 
"""
@shared_task
def send_reminder(*args, **kwargs):
    taskmanager.get_customers_to_send_reminder()
    
"""
Crontab to send scheduler reminder sms setup by admin
"""
@shared_task
def send_schedule_reminder(*args, **kwargs):
    taskmanager.get_customers_to_send_reminder_by_admin()


"""
Crontab to set the is_expire=True for all those coupon which expire till current date time
"""
@shared_task
def expire_service_coupon(*args, **kwargs):
    taskmanager.expire_service_coupon()

"""
Crontab to import data from SAP to Gladminds Database
"""
@shared_task
def import_data(*args, **kwargs):
    print "import data from SAP CRM to MySQL"

