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
        'USER': 'root',
        'PASSWORD': 'hasher123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


BROKER_URL = 'redis://localhost:6379'
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

######################################################
#ADDED SETTINGS TO TEST CAPSYSTEM ON DEV ENV
###########################################################
ENABLE_AMAZON_SQS = False

FILE_CACHE_DURATION = 0
SMS_CLIENT = "KAP"
  
# SMS_CLIENT_DETAIL = {
#                      'OTP_TWILIO_ACCOUNT' : 'ACbb8cb45f6113b8f2f6243c8eaa5ff971',
#                      'OTP_TWILIO_AUTH' : 'aa445a4f0a7e651738e89810601f8860',
#                      'OTP_TWILIO_FROM' : '+1 469-513-9856',
#                      'OTP_TWILIO_URI' : 'https://api.twilio.com/2010-04-01/Accounts/{0}/Messages.json'
#                 }
########################SQS Queue Name
SQS_QUEUE_NAME = "gladminds-dev"
######################################

FEED_TYPE = 'CSV'
FEED_FAILURE_MAIL_ENABLED = True

MAIL_DETAIL["subject"] = "GladMinds Feed Report DEV"
MAIL_DETAIL["receiver"] = ["naureen.razi@hashedin.com"]

FEED_FAILURE_MAIL_DETAIL["subject"] = "GladMinds Feed Failure Mail DEV"
FEED_FAILURE_MAIL_DETAIL["receiver"] = ["naureen.razi@hashedin.com"]
UCN_RECOVERY_MAIL_DETAIL["subject"] = "GladMinds UCN Recovery Mail DEV"
VIN_DOES_NOT_EXIST_DETAIL["receiver"] = ["srv.sngh92@yahoo.com","priyanka.n@hashedin.com","somit@hashedin.com","suresh@hashedin.com","chandan.patel@hashedin.com","naureen.razi@hashedin.com"]

#############################################################################
LOGGING['handlers']['gladminds_logs']['filename'] = 'log/gladminds/app/gladminds.log'
LOGGING['handlers']['afterbuy_logs']['filename'] = 'log/gladminds/app/afterbuy.log'
