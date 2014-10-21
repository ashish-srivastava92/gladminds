from django.utils import timezone

from gladminds.bajaj.models import AuditLog, DataFeedLog


def audit_log(action='SENT', sender='+1 469-513-9856', reciever=None,
              message=None, status='success'):
    if reciever == '9999999999':
        status = 'fail'

    action_log = AuditLog(date=timezone.now(),
                               action=action, sender=sender,
                               reciever=reciever, status=status,
                               message=message)
    action_log.save()


def feed_log(feed_type=None, total_data_count=None, failed_data_count=None,
     success_data_count=None, status=None, action=None, remarks=None, file_location=None):

    data_feed_log = DataFeedLog(feed_type=feed_type,
                                     total_data_count=total_data_count,
                                     failed_data_count=failed_data_count,
                                     success_data_count=success_data_count,
                                     status=status, action=action,
                                     remarks=remarks, file_location=file_location)
    data_feed_log.save()


