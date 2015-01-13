# Django settings for gladminds project.
import os
import djcelery
djcelery.setup_loader()
DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
BASE_DIR = os.path.join(PROJECT_DIR, os.pardir)
STATIC_DIR = os.path.join(PROJECT_DIR, "static")
TEMPLATE_DIR = os.path.join(PROJECT_DIR, "templates")
EMAIL_DIR = os.path.join(TEMPLATE_DIR, "email")
DATA_CSV_PATH = os.path.join(BASE_DIR, "src/data")

TIMEZONE = 'Asia/Kolkata'

ALLOWED_HOSTS = ['*']

ALLOWED_KEYWORDS = {'register': 'gcp_reg', 'service':
                    'service', 'check': 'a', 'close': 'c', 'brand': 'brand',
                    'service_desk': 'sd', 'customer_detail_recovery': 'r',
                    'accumulate_point':'ac', 'redeem_point':'rd'}

ADMINS = (
    ('somit', 'somit@hashedin.com'),
    ('naureen', 'naureen.razi@hashedin.com'),
    ('priyanka', 'priyanka.n@hashedin.com')
)
API_FLAG = False
COUPON_VALID_DAYS = 30
COUPON_URL = 'local.bajaj.gladmindsplatform.co'
TOTP_SECRET_KEY = '93424'
OTP_VALIDITY = 120
HARCODED_OTPS = ['000000']
HARCODED_TOKEN = ['e6281aa90743296987089ab013ee245dab66b27b']
IGNORE_ENV = ['dev', 'local', 'test']
PASSWORD_REST_URL = ''
ACCOUNT_ACTIVATION_DAYS = 10
DOMAIN_BASE_URL = '/afterbuy/v1/consumers/activate-email/'
OAUTH_DELETE_EXPIRED = True
JOBCARD_DIR = '{0}/jobcards/prod/'
JOBCARD_BUCKET = 'gladminds'

FEED_FAILURE_DIR = 'aftersell/{0}/feed-logs/qa/'
FEED_FAILURE_BUCKET = 'gladminds'

S3_ID = 'AKIAIL7IDCSTNCG2R6JA'
S3_KEY = '+5iYfw0LzN8gPNONTSEtyUfmsauUchW1bLX3QL9A'

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'gladminds.core.context_processors.gm_constants',
    'django.core.context_processors.request',
)

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
        {'app': 'bajaj', 'label': 'Loyalty', 'icon': ' icon-folder-open',
         'models':(
                    {'model': 'nationalsalesmanager',
                     'label': 'National Sales Manager'},
                   {'model': 'areasalesmanager',
                     'label': 'Area Sales Manager'},
                    {'model': 'distributor',
                     'label': 'Distributor'},
                   {'model': 'mechanic',
                     'label': 'Mechanic'},
                   {'model': 'sparepartmasterdata',
                     'label': 'Spare Part Master Data'},
                   {'model': 'sparepartupc',
                     'label': 'Spare Part UPC'},
                   {'model': 'sparepartpoint',
                     'label': 'Spare Part Point'},
                   {'model': 'accumulationrequest',
                     'label': 'Accumulation Request'},)},
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


MANAGERS = ADMINS

DATABASE_ROUTERS = ['gladminds.router.DatabaseAppsRouter']

# Mapping is first app name then db name
DATABASE_APPS_MAPPING = {
                         'default': 'default',
                         'bajaj':'bajaj',
                         'demo': 'demo',
                         'afterbuy':'afterbuy'
                    }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'gm',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'bajaj': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bajaj',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'demo': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'demo',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'afterbuy': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'afterbuy',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Calcutta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = 'afterbuy.s3-website-us-east-1.amazonaws.com'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, "gladminds", 'collected')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    STATIC_DIR,
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
   # 'gladminds.core.custom_staticfiles_loader.FileSystemFinder',                   
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bbu7*-yvup0-*laxug+n5tf^lga_bwtrxu%y4ilb#$lv8%zw0m'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
                    # for performance enable cached templates
                    #      ('django.template.loaders.cached.Loader', (
                    #         'django.template.loaders.filesystem.Loader',
                    #         'django.template.loaders.app_directories.Loader',
                    #     )),
                    'gladminds.core.loaders.custom_template_loader.Loader',
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    #  'django.template.loaders.eggs.Loader',
                   )

MIDDLEWARE_CLASSES = (
    'gladminds.core.middlewares.dynamicsite_middleware.DynamicSitesMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'gladminds.core.middlewares.middleware.GladmindsMessageMiddleware',
#     'gladminds.middleware.GladmindsMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
                     )

CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'gladminds.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'gladminds.wsgi.application'

TEMPLATE_DIRS = (
    TEMPLATE_DIR,
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEST_IGNORE_APPS = (# 'south',
                    )

ALL_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'suit',
    'django.contrib.admin',
    'import_export',
    'provider',
    'provider.oauth2',
    'gladminds',
    'gladminds.default',
    'gladminds.core',
    'gladminds.bajaj',
    'gladminds.demo',
    'gladminds.afterbuy',
    'djcelery',
    'corsheaders',
    'storages',
    'tastypie_swagger',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'constance.backends.database'
   # 'debug_toolbar',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

INSTALLED_APPS = ALL_APPS + TEST_IGNORE_APPS

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


LOGIN_REDIRECT_URL = '/register/redirect'

TASTYPIE_SWAGGER_API_MODULE = 'gladminds.urls.api_v1'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(name)-20s: %(levelname)-8s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
         'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'sql': {
            'level': 'DEBUG',
            'filename': '/var/log/gladminds/sql.log',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
        },
        'gladminds_logs': {
            'level': 'INFO',
            'filename': '/var/log/gladminds/gladminds.log',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
        },
        'afterbuy_logs': {
            'level': 'INFO',
            'filename': '/var/log/gladminds/afterbuy.log',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
        }
    },

    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['sql'],
            'propagate': True,
        },
        'gladminds': {
            'handlers': ['gladminds_logs', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'spyne': {
            'handlers': ['gladminds_logs', 'console'],
            'level': 'WARN',
            'propagate': True,
        }, 'afterbuy': {
            'handlers': ['afterbuy_logs', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}


CUSTOMER_REGISTRATION_WSDL = 'qa_customer_registration.wsdl'
COUPON_WSDL = 'qa_coupon_redeem.wsdl'
VIN_SYNC_WSDL='qa_vin_sync.wsdl'

MAIL_SERVER = 'localhost'
MAIL_DETAIL = {
    "sender": "feed-report@gladminds.co",
    "receiver": ["gladminds@hashedin.com", "naveen.shankar@gladminds.co"],
    "subject": "Gladminds Feed Report",
    "body": """""",
}

FEED_FAILURE = {
    "sender": "feed-report@gladminds.co",
    "receiver": ["gladminds@hashedin.com"],
    "subject": "Gladminds Failure Report - ",
    "body": """""",
}

VIN_SYNC_FEED = {
                 "receiver": ["priyanka.n@hashedin.com"],
                 }

CUSTOMER_PHONE_NUMBER_UPDATE = {

    "sender": "feed-report@gladminds.co",
    "receiver": ["gladminds@hashedin.com"],
    "subject": "Gladminds customer phone number update",
    "body": """""",
}

UCN_RECOVERY_MAIL_DETAIL = {
                            "sender": "feed-report@gladminds.co",
                            "receiver": ["gladminds@hashedin.com"],
                            "subject": "Gladminds UCN Recovery Mail",
                            "body": """""",
                           }

VIN_DOES_NOT_EXIST_DETAIL = {
    "sender": "support@gladminds.co",
    "receiver": [],
    "subject": "Request for Dispatch feed",
    "body": """""",
}

REGISTER_ASC_MAIL_DETAIL = {
    "sender": "support@gladminds.co",
    "receiver": [],
    "subject": "ASC Registration Mail",
    "body": """""",
}

OTP_MAIL = {
                  "sender":"support@gladminds.co",
                  "subject":"Reset Password",
                  "receiver": [""],
                  "body": """""",
              }

PASSWORD_RESET_MAIL = {
                  "sender":"support@gladminds.co",
                  "subject":"Reset Password",
                  "receiver": [""],
                  "body": """""",
              }

EMAIL_ACTIVATION_MAIL = {
                  "sender":"support@gladminds.co",
                  "subject":"Confirm your email address",
                  "receiver": [""],
                  "body": """""", }

RECYCLE_MAIL = {
                "sender":"support@gladminds.co",
                "subject":"Product for recycle",
                "receiver": ["demosupport@gladminds.co"],
                "body": """""",
                
                }

# AfterBuy File Upload location configuration
AFTERBUY_LOC = os.path.join(PROJECT_DIR, "afterbuy")
AFTERBUY_USER_LOC = os.path.join(AFTERBUY_LOC, "users")
AFTERBUY_PRODUCT_LOC = os.path.join(AFTERBUY_LOC, "products")
AFTERBUY_BRAND_LOC = os.path.join(AFTERBUY_LOC, "brands")
AFTERBUY_PRODUCT_TYPE_LOC = os.path.join(AFTERBUY_LOC, "productType")
AFTERBUY_PRODUCT_WARRENTY_LOC = os.path.join(AFTERBUY_PRODUCT_LOC, "warrenty")
AFTERBUY_PRODUCT_INSURANCE_LOC = os.path.join(
    AFTERBUY_PRODUCT_LOC, "insurance")
AFTERBUY_PRODUCT_INVOICE_LOC = os.path.join(AFTERBUY_PRODUCT_LOC, "invoice")
MEDIA_ROOT = AFTERBUY_LOC
MEDIA_URL = '/media/'

# S3 Configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_STORAGE_BUCKET_MAP = {'afterbuy': 'afterbuy'}
AWS_STORAGE_BUCKET_NAME = 'gladminds-brands'
S3_BASE_URL = 'https://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
ALLOWED_IMAGE_TYPES = ['jpg', 'jpeg', 'png', 'gif']
MAX_UPLOAD_IMAGE_SIZE = 4.0


DEFAULT_COUPON_STATUS = 1
DELAY_IN_CUSTOMER_UCN_MESSAGE = 5
ENABLE_AMAZON_SQS = False

#################Registration Configuration#################################
REGISTRATION_CONFIG = {
                        "bajaj": {
                            "ASC Registration Feed": {
                                "retry_time": 180,
                                "num_of_retry": 2,
                                "delay": 180,
                                "fail_mail_detail": {
                                    "sender": "feed-report@gladminds.co",
                                    "receiver": "naureen.razi@hashedin.com",
                                    "subject": "Gladminds ASC Registration Fail",
                                    "body": """"""
                                }
                            }
                        }
                     }
###########################################################################
########################Password Postfix for dealers######################
PASSWORD_POSTFIX = '@123'
TEMP_ID_PREFIX = 'T'
TEMP_SA_ID_PREFIX = 'SA'
###########################################################################
########################Feed Failure Mail enabled ######################
FEED_FAILURE_MAIL_ENABLED = True
##########################################################################
#########################New relic file location########################
NEW_RELIC_FILE_LOCATION = './src/'
########################################################################
#######################SMS_HEALTH_CHECK_INTERVAL
SMS_HEALTH_CHECK_INTERVAL = 6
#######################FEED_HEALTH_CHECK_INTERVAL
FEED_HEALTH_CHECK_INTERVAL = 8
################################################
BRAND = 'bajaj'
GM_BRAND = 'default'
BRANDS = ['bajaj', 'demo', 'afterbuy']
###############################################
AIRTEL_IP = '54.84.243.77'
SMS_CLIENT = "AIRTEL"
SMS_CLIENT_DETAIL = { 'AIRTEL': {'login':'bajajauto',
                              'pass':'bajaj',
                              'authenticate_url':'http://117.99.128.32:80/login/pushsms.php',
                              'message_url': 'http://117.99.128.32:80/login/pushsms.php'},
                  'KAP': {'login':'GladMinds1',
                          'pass':'kap@user!23',
                          'message_url': 'http://alerts.kapsystem.com/api/web2sms.php',
                          'working_key': '2uj6gnnnlbx37x436cppq87176j660w9',
                          'sender_id': 'GLADMS',
                          'params': 'kap'}
                  }

ADMIN_DETAILS = {'bajaj': {'user': 'bajaj', 'password': 'bajaj'},
          'demo': {'user': 'demo', 'password': 'demo'},
          'afterbuy': {'user': 'afterbuy', 'password': 'afterbuy'},
          'default': {'user': 'gladminds', 'password': 'gladminds'}
          }
##################################################################################################
ENABLE_SERVICE_DESK = True

DEFAULT_IMAGE_ID = 'guest.png'

CONSTANCE_CONFIG = {
    'DEFAULT_IMAGE': ('guest.png', 'Default image to be used by any app'),
    'AFTERBUY_FORGOT_PASSWORD_URL': ('http://afterbuy.co/demo/staging_qw741qaz5/change-password.php', 'Afterbuy forgot password url'),
    'AFTERBUY_RECYCLE_EMAIL_RECIPIENT' : ('demosupport@gladminds.co', 'Default Email for recycle')
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
