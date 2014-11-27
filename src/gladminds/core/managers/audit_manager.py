from gladminds.bajaj.models import DataFeedLog
from gladminds.core.utils import get_model


def sms_log(action='SENT', sender='+1 469-513-9856', receiver=None,
              message=None, status='success', brand='bajaj'):
    if receiver == '9999999999':
        status = 'fail'
    sm_model = get_model('SMSLog', brand)
    sms_log = sm_model(action=action, sender=sender,
                               receiver=receiver, status=status,
                               message=message)
    sms_log.save()


def feed_log(feed_type=None, total_data_count=None, failed_data_count=None,
     success_data_count=None, status=None, action=None, remarks=None, file_location=None):

    data_feed_log = DataFeedLog(feed_type=feed_type,
                                     total_data_count=total_data_count,
                                     failed_data_count=failed_data_count,
                                     success_data_count=success_data_count,
                                     status=status, action=action,
                                     remarks=remarks, file_location=file_location)
    data_feed_log.save()
    