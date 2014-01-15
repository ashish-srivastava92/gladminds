from __future__ import absolute_import
from celery import shared_task
from gladminds.utils import save_log
from gladminds.dao.smsclient import MockSmsClient as smsclient
from gladminds.resource.resources import GladmindsTaskManager
import logging
logger = logging.getLogger(__name__)


@shared_task
def send_registration_detail(**kwargs):
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = smsclient.send_stateless(**kwargs)
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        print debug_message
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
def send_service_detail(**kwargs):
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        response_data = smsclient.send_stateless(**kwargs)
        
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        print debug_message
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
def send_coupon_validity_detail(**kwargs):
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = smsclient.send_stateless(**kwargs)
        
        debug_message = "Send the message: %s To : %s" % (phone_number, message)
        print debug_message
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
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = smsclient.send_stateless(**kwargs)
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

