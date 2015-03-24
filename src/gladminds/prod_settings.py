# pylint: disable=W0401,W0614
import os
from settings import *

PROJECT_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
BASE_DIR = os.path.join(PROJECT_DIR, os.pardir)
STATIC_DIR = os.path.join(BASE_DIR, "src/static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "src/templates")
OUT_DIR = os.path.join(BASE_DIR, "out")

DB_PASSWORD = os.environ.get('DB_PASSWORD')

DEBUG = False
ALLOWED_HOSTS = ['*']
TEMPLATE_DEBUG = DEBUG

MEDIA_ROOT = 'afterbuy.s3-website-us-east-1.amazonaws.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gm',
        'USER': 'gladminds',
        'PASSWORD': DB_PASSWORD,
        'HOST': 'gladminds-prod.chnnvvffqwop.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    },
    'bajaj': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bajaj',
        'USER': 'gladminds',
        'PASSWORD': DB_PASSWORD,
        'HOST': 'gladminds-prod.chnnvvffqwop.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    },
    'demo': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demo',
        'USER': 'gladminds',
        'PASSWORD': DB_PASSWORD,
        'HOST': 'gladminds-prod.chnnvvffqwop.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    },
    'afterbuy': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'afterbuy',
        'USER': 'gladminds',
        'PASSWORD': DB_PASSWORD,
        'HOST': 'gladminds-prod.chnnvvffqwop.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}



BROKER_URL = 'redis://localhost:6379'
REDIS_URL = 'redis://localhost:6379'


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

# SMS_CLIENT = "TWILIO"
#  SMS_CLIENT_DETAIL = {
#                      'OTP_TWILIO_ACCOUNT' : 'ACbb8cb45f6113b8f2f6243c8eaa5ff971',
#                      'OTP_TWILIO_AUTH' : 'aa445a4f0a7e651738e89810601f8860',
#                      'OTP_TWILIO_FROM' : '+1 469-513-9856',
#                      'OTP_TWILIO_URI' : 'https://api.twilio.com/2010-04-01/Accounts/{0}/Messages.json'
#                 }

FILE_CACHE_DURATION = 1800

FEED_TYPE = 'CSV'

SMS_CLIENT = "AIRTEL"

#AfterBuy File Upload location configuration
AFTERBUY_LOC = os.path.join(PROJECT_DIR, "afterbuy")
AFTERBUY_USER_LOC = os.path.join(AFTERBUY_LOC, "users")
AFTERBUY_PRODUCT_LOC = os.path.join(AFTERBUY_LOC, "products")
AFTERBUY_BRAND_LOC = os.path.join(AFTERBUY_LOC, "brands")
AFTERBUY_PRODUCT_TYPE_LOC = os.path.join(AFTERBUY_LOC, "productType")
AFTERBUY_PRODUCT_WARRENTY_LOC = os.path.join(AFTERBUY_PRODUCT_LOC, "warrenty")
AFTERBUY_PRODUCT_INSURANCE_LOC = os.path.join(AFTERBUY_PRODUCT_LOC, "insurance")
AFTERBUY_PRODUCT_INVOICE_LOC = os.path.join(AFTERBUY_PRODUCT_LOC, "invoice")
MEDIA_ROOT = AFTERBUY_LOC
MEDIA_URL = '/media/'


#S3 Configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

SAP_CRM_DETAIL = {
                  'username':'pisuper',
                  'password':'welcome123'
                  }

COUPON_WSDL = 'prod_coupon_redeem.wsdl'
CUSTOMER_REGISTRATION_WSDL = 'prod_customer_registration.wsdl'
VIN_SYNC_WSDL='prod_vin_sync.wsdl'
PURCHASE_SYNC_WSDL='prod_purchase_sync_feed.wsdl'


ASC_WSDL_URL = "http://bajaj.gladminds.co/api/v1/asc-feed/?wsdl&v0"
COUPON_WSDL_URL = "http://bajaj.gladminds.co/api/v1/coupon-redeem/?wsdl&v0"
CUSTOMER_REGISTRATION_WSDL_URL = "http://bajaj.gladminds.co/api/v1/customer-feed/?wsdl&v0"
VIN_SYNC_WSDL_URL="http://bajaj.gladminds.co/api/v1/vin-sync/?wsdl&v0"
PURCHASE_SYNC_WSDL_URL="http://bajaj.gladminds.co/api/v1/purchase-sync/?wsdl&v0"


ENABLE_AMAZON_SQS = True

AFTER_BUY_CONSTANTS = {
                       "username": 'support@gladminds.com',
                       "password": 'gladminds123',
                       "key_prefix": 'qa',
                       "app_path": 'afterbuy_script/afterbuy.zip',
                       "phonegap_build_url": 'https://build.phonegap.com/',
                       "try_count": 300,
                       "android_apk_loc": "afterbuy_script/qa_android_afterbuy.apk",
                       "ios_apk_loc": "afterbuy_script/qa_ios_afterbuy.ipa",
                       "create_method": "file",
                       "package": "com.gladminds.afterbuyv1",
                       "version": "0.1.0",
                       "title": "Afterbuy V1 App"
                       }

########################SQS Queue Name##################################
SQS_QUEUE_NAME = "gladminds-prod2"
SQS_QUEUE_NAME_SMS = "gladminds-prod-sms"
########################################################################
UCN_RECOVERY_MAIL_DETAIL["subject"] = "GladMinds UCN Recovery Mail"
UCN_RECOVERY_MAIL_DETAIL["receiver"] = ["suresh@hashedin.com", "gladminds@hashedin.com", "nvhasabnis@bajajauto.co.in", "ssozarde@bajajauto.co.in","jojibabu.vege@gladminds.co","support@gladminds.co"]
VIN_DOES_NOT_EXIST_DETAIL["receiver"] = ["suresh@hashedin.com", "jojibabu.vege@gladminds.co","ssozarde@bajajauto.co.in", "gladminds@hashedin.com", "Dhazarika@bajajauto.co.in", "Rkjena@bajajauto.co.in", "skolluri@bajajauto.co.in", "sudhir.patil@gladminds.co"]
FEED_FAILURE["subject"] = "Consolidated Report: GladMinds Feed Failure - "
FEED_FAILURE["receiver"] = ["suresh@hashedin.com", "jojibabu.vege@gladminds.co", "ssozarde@bajajauto.co.in", "skolluri@bajajauto.co.in",
                            "sudhir.patil@gladminds.co", "rkjena@bajajauto.co.in", "dhazarika@bajajauto.co.in",
                            "gladminds@hashedin.com", "naveen.shankar@gladminds.co"]
CUSTOMER_PHONE_NUMBER_UPDATE["receiver"] = ["suresh@hashedin.com", "jojibabu.vege@gladminds.co", "ssozarde@bajajauto.co.in",
                                            "skolluri@bajajauto.co.in", "sudhir.patil@gladminds.co",
                                            "rkjena@bajajauto.co.in", "dhazarika@bajajauto.co.in",
                                            "gladminds@hashedin.com"]
VIN_SYNC_FEED["receiver"] = ["suresh@hashedin.com", "rkjena@bajajauto.co.in", "dhazarika@bajajauto.co.in", "ssozarde@bajajauto.co.in", "gladminds@hashedin.com"]

POLICY_DISCREPANCY_MAIL_TO_MANAGER ["receiver"] = ["suresh@hashedin.com", "jojibabu.vege@gladminds.co", "ssozarde@bajajauto.co.in",
                                                   "sudhir.patil@gladminds.co", "rkjena@bajajauto.co.in", "dhazarika@bajajauto.co.in",
                                                   "gladminds@hashedin.com", "naveen.shankar@gladminds.co"]
########################################################################
###################Change Mail Subject on Prod##########################
MAIL_DETAIL["subject"] = "Report: GladMinds Feed Summary"
MAIL_DETAIL["receiver"] = ["jojibabu.vege@gladminds.co", "ssozarde@bajajauto.co.in", "skolluri@bajajauto.co.in",
                            "sudhir.patil@gladminds.co", "rkjena@bajajauto.co.in", "dhazarika@bajajauto.co.in",
                            "gladminds@hashedin.com", "suresh@hashedin.com", "naveen.shankar@gladminds.co", "sudhir.patil@gladminds.co"]

#######################Feed Fail Failure Info###########################
FEED_FAILURE_DIR = 'aftersell/{0}/feed-logs/dev/'
FEED_FAILURE_BUCKET = 'gladminds'
#######################################################################
ENABLE_SERVICE_DESK = False
ENV = "prod"

WSDL_TNS="http://bajaj.gladminds.co/api/v1/feed/"

ADMIN_DETAILS = {'bajaj': {'user': 'bajaj001', 'password': 'bajaj001'},
          'demo': {'user': 'demo', 'password': 'demo'},
          'afterbuy': {'user': 'afterbuy', 'password': 'afterbuy'},
          'default': {'user': 'gladminds', 'password': 'gladminds'}
          }


SUIT_CONFIG = {
    'ADMIN_NAME': 'GladMinds',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SEARCH_URL': '',
    'MENU_EXCLUDE': ('auth.group', 'auth', 'sites'),
    'MENU_OPEN_FIRST_CHILD': True,
    'LIST_PER_PAGE': 20,
    'SHOW_REQUIRED_ASTERISK': True,
    'MENU': (
        {'app': 'bajaj', 'label': 'Users', 'icon': ' icon-folder-open',
         'models': ('user', 'userprofile',
                    {'model': 'dealer',
                     'label': 'Dealer'},
                    {'model': 'authorizedservicecenter',
                     'label': 'Authorized Service Center'},
                    {'model': 'serviceadvisor',
                     'label': 'Service Advisor'},)},
        {'app': 'bajaj', 'label': 'Products', 'icon': ' icon-folder-open',
         'models':({'model': 'brandproductcategory',
                     'label': 'Brand Product Category'},
                    {'model': 'producttype',
                     'label': 'Product Type'},
                    {'model': 'dispatchedproduct',
                     'label': 'Product Dispatch'},
                    {'model': 'productdata',
                     'label': 'Product Purchase'},
                    {'model': 'coupondata',
                     'label': 'Coupon Redemption'},)},
        {'app': 'bajaj', 'label': 'Logs', 'icon': ' icon-folder-open',
         'models':(
                    {'model': 'smslog',
                     'label': 'SMS Log'},
                   {'model': 'emaillog',
                     'label': 'Email Log'},
                    {'model': 'datafeedlog',
                     'label': 'Feed Log'},
                   {'model': 'feedFailureLog',
                     'label': 'Feed Failure Log'})},
        {'app': 'bajaj', 'label': 'User Registrations', 'icon': ' icon-folder-open',
         'models':(
                    {'model': 'asctempregistration',
                     'label': ' ASC registration'},
                    {'model': 'satempregistration',
                     'label': 'SA registration'},
                    {'model': 'customertempregistration',
                     'label': ' Customer registration'},)},
        {'app': 'bajaj', 'label': 'Templates', 'icon': ' icon-folder-open',
         'models':(
                    'messagetemplate', 'emailtemplate',)},)
}


# CACHES = {
#     'default': {
#         'BACKEND': 'django_elasticache.memcached.ElastiCache',
#         'LOCATION': 'gladminds-memcache.t2nfas.cfg.use1.cache.amazonaws.com:11211'
#     }
# }
