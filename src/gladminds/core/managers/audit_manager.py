from gladminds.core.loaders.module_loader import get_model
import datetime


def sms_log(action='SENT', sender='+1 469-513-9856', receiver=None,
              message=None, status='success', brand='bajaj'):
    if receiver == '9999999999':
        status = 'fail'
    sm_model = get_model('SMSLog', brand=brand)
    sms_log = sm_model(action=action, sender=sender,
                               receiver=receiver, status=status,
                               message=message)
    sms_log.save()


def feed_log(feed_type=None, total_data_count=None, failed_data_count=None,
     success_data_count=None, status=None, action=None, remarks=None, file_location=None, brand='bajaj'):

    feed_log_model = get_model('DataFeedLog', brand=brand)
    data_feed_log = feed_log_model(feed_type=feed_type,
                                     total_data_count=total_data_count,
                                     failed_data_count=failed_data_count,
                                     success_data_count=success_data_count,
                                     status=status, action=action,
                                     remarks=remarks, file_location=file_location)
    data_feed_log.save()

def email_log(subject, message, sender, receiver, brand='bajaj'):
    email_model = get_model('EmailLog', brand=brand)
    email_log = email_model(subject=subject, message=message, sender=sender, receiver=receiver)
    email_log.save()

def feed_failure_log(feed_type=None, reason=None, brand='bajaj'):

    feed_failure_log_model = get_model('FeedFailureLog', brand=brand)
    feed_failure_log = feed_failure_log_model(feed_type=feed_type,
                                     reason=reason, created_date=datetime.datetime.now())
    feed_failure_log.save()
    