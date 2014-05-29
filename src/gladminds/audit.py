from django.utils import timezone

from gladminds.aftersell.models import logs
from collections import Counter
import json


def audit_log(action='SENT', sender='+1 469-513-9856', reciever=None,
              message=None, status='success'):
    if reciever == '9999999999':
        status = 'fail'

    action_log = logs.AuditLog(date=timezone.now(),
                               action=action, sender=sender,
                               reciever=reciever, status=status,
                               message=message)
    action_log.save()


def feed_log(feed_type=None, total_data_count=None, failed_data_count=None,
             success_data_count=None, status=None, action=None, remarks=None):

    data_feed_log = logs.DataFeedLog(feed_type=feed_type,
                                     total_data_count=total_data_count,
                                     failed_data_count=failed_data_count,
                                     success_data_count=success_data_count,
                                     status=status, action=action,
                                     remarks=remarks)
    data_feed_log.save()


class FeedLogWithRemark():

    def __init__(self, total_feeds, feed_type, action, status):
        self.total_feeds = total_feeds
        self.failed_feeds = 0
        self.feed_type = feed_type
        self.action = action
        self.status = status
        self.remarks = Counter()

    def fail_remarks(self, remark):
        self.remarks[remark] += 1
        self.failed_feeds = self.failed_feeds + 1

    def save_to_feed_log(self):
        success_data_count = self.total_feeds - self.failed_feeds
        remarks = json.dumps(self.remarks)
        feed_log(feed_type=self.feed_type, total_data_count=self.total_feeds,
              failed_data_count=self.failed_feeds,
              success_data_count=success_data_count, status=self.status,
              action=self.action, remarks=remarks)
