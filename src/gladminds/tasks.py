from __future__ import absolute_import
from celery import shared_task
from gladminds.utils import save_log
import logging
logger = logging.getLogger(__name__)


@shared_task
def send_message(**kwargs):
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
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
        send_message.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries = 5)

@shared_task
def send_reminder(*args, **kwargs):
    print "Sent reminder to customer"

@shared_task
def import_data(*args, **kwargs):
    print "import data from SAP CRM to MySQL"