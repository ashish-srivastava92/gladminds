# pylint: disable=W0401,W0614
import os
from settings import *

PROJECT_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
BASE_DIR = os.path.join(PROJECT_DIR, os.pardir)
STATIC_DIR = os.path.join(BASE_DIR, "src/static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "src/templates")
OUT_DIR = os.path.join(BASE_DIR, "out")

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gladmindsdb',
        'USER': 'gladminds',
        'PASSWORD': 'gladminds123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


BROKER_URL= 'redis://localhost:6379'
REDIS_URL = 'redis://localhost:6379'


JOBCARD_DIR = '{0}/jobcards/dev/'

FEED_FAILURE_DIR = 'aftersell/{0}/feed-logs/dev/'
FEED_FAILURE_BUCKET = 'gladminds'

MAIL_SERVER = 'localhost'


STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    STATIC_DIR,
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_DIR,
)

ENABLE_AMAZON_SQS = True

SMS_CLIENT = "KAP"
SMS_CLIENT_DETAIL={
                   'login':'GladMinds1',
                   'pass':'kap@user!23',
                   'message_url': 'http://alerts.kapsystem.com/api/web2sms.php',
                   'working_key': '1486415t035t8052c7pc',
                   'sender_id': 'GLADMS'     
                   }


########################SQS Queue Name
SQS_QUEUE_NAME = "gladminds-test"
######################################

FEED_TYPE = 'CSV'
FEED_FAILURE_MAIL_ENABLED = True

MAIL_DETAIL["subject"]= "GladMinds Feed Report DEV"
MAIL_DETAIL["receiver"] = ["naureen.razi@hashedin.com"]

FEED_FAILURE_MAIL_DETAIL["subject"] = "GladMinds Feed Failure Mail DEV"
FEED_FAILURE_MAIL_DETAIL["receiver"] = ["naureen.razi@hashedin.com"]
UCN_RECOVERY_MAIL_DETAIL["subject"] = "GladMinds UCN Recovery Mail DEV"
