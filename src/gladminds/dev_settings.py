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
        'NAME': 'gladminds',
        'USER': 'gladminds',
        'PASSWORD': 'gladmindsRocks',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

TNS = "http://api.gladmindsplatform.co/api/v1/bajaj/feed/"

BROKER_URL= 'redis://localhost:6379'
REDIS_URL = 'redis://localhost:6379'

JOBCARD_DIR = '/jobcards/dev'

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

# SMS_CLIENT = "MOCK"
# SMS_CLIENT_DETAIL = {
#                      'OTP_TWILIO_ACCOUNT' : 'ACbb8cb45f6113b8f2f6243c8eaa5ff971',
#                      'OTP_TWILIO_AUTH' : 'aa445a4f0a7e651738e89810601f8860',
#                      'OTP_TWILIO_FROM' : '+1 469-513-9856',
#                      'OTP_TWILIO_URI' : 'https://api.twilio.com/2010-04-01/Accounts/{0}/Messages.json'
#                 }

SMS_CLIENT = "AIRTEL"
SMS_CLIENT_DETAIL={
                    'login':'bajajauto',
                    'pass':'bajaj',
                    'authenticate_url':'http://117.99.128.32:80/login/pushsms.php' ,
                    'message_url': 'http://117.99.128.32:80/login/pushsms.php'                  
                    }

FEED_TYPE = 'CSV'

SAP_CRM_DETAIL = {
                  'username': 'gladminds',
                  'password': 'gladminds'
                  }
COUPON_WSDL_URL = "localhost:8000/api/v1/bajaj/redeem-feed/?wsdl"
ASC_WSDL_URL = "localhost:8000/api/v1/bajaj/asc-feed/?wsdl&v0"

MAIL_SERVER = 'localhost'
