from __future__ import absolute_import
from celery import shared_task
from django.conf import settings
from gladminds.utils import save_log
from gladminds.dao.smsclient import MockSmsClient
from gladminds.tasksmanager import GladmindsTaskManager
import logging
logger = logging.getLogger(__name__)

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

@shared_task
def send_reminder(*args, **kwargs):
    obj = GladmindsTaskManager()
    obj.get_customers_to_send_reminder()
    

def send_reminder_message(*args, **kwargs):
    try:
        client = settings.SMS_CLIENT_DETAIL
        sms_client = MockSmsClient(**client)
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = mock_client.send_stateless(**kwargs)
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
    

@shared_task
def import_data(*args, **kwargs):
    print "import data from SAP CRM to MySQL"

