from __future__ import absolute_import
from celery import shared_task

@shared_task
def send_message(**kwargs):
    mobile_number = kwargs.get('mobile_number', None)
    message = kwargs.get('message', None)
    pass
