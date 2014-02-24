from datetime import datetime
from django.conf import settings

from models import logs


def audit_log(action='SENT', sender='+1 574-212-0423', reciever=None, message=None, status='success'):
    if reciever=='9999999999':
        status='fail'
        kwargs = {
                    'action':action,
                    'reciever': reciever,
                    'sender':'sender',
                    'message': message,
                    'status':'fail'
                }
    else:
        kwargs = {
                    'action':action,
                    'reciever': reciever,
                    'sender':'sender',
                    'message': message,
                    'status':status
                }
        
    action_log = logs.AuditLog(date=datetime.now(), action=action, sender=sender, reciever=reciever, status=status, message=message)
    action_log.save()

def feed_log(feed_type = None, total_data_count = None, failed_data_count = None, success_data_count = None, status = None, action = None):
    data_feed_log = logs.DataFeedLog(feed_type = feed_type, total_data_count = total_data_count, failed_data_count = failed_data_count, success_data_count = success_data_count, status = status, action = action)
    data_feed_log.save()