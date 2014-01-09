from __future__ import absolute_import
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_message(**kwargs):
    phone_number = kwargs.get('phone_number', None)
    message = kwargs.get('message', None)
    debug_message = "Send the message: %s To : %s" % (phone_number, message)
    print debug_message
    logger.info(debug_message)
