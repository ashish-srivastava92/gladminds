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
DATA_CSV_PATH = os.path.join(BASE_DIR, "src/data")

ALLOWED_HOSTS = ['*']

ALLOWED_KEYWORDS = {'register': 'gcp_reg', 'service':
                    'service', 'check': 'a', 'close': 'c', 'brand': 'brand',
                    'customer_detail_recovery': 'r'}
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

COUPON_VALID_DAYS = 30

TOTP_SECRET_KEY = '93424'
OTP_VALIDITY = 120

JOBCARD_DIR = '{0}/jobcards/prod/'
JOBCARD_BUCKET = 'gladminds'

FEED_FAILURE_DIR = 'aftersell/{0}/feed-logs/qa/'
FEED_FAILURE_BUCKET = 'gladminds'

S3_ID = 'AKIAIL7IDCSTNCG2R6JA'
S3_KEY = '+5iYfw0LzN8gPNONTSEtyUfmsauUchW1bLX3QL9A'

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
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
        {'app': 'gladminds', 'label': 'Data', 'icon': ' icon-folder-open',
         'models': ({'model': 'serviceadvisordealerrelationship', 'label': 'Feed -> Service Advisor'},
                    {'model': 'dispatchedproduct',
                     'label': 'Feed -> Product Dispatch'},
                    {'model': 'productdata',
                     'label': 'Feed -> Product Purchase'},
                    {'model': 'coupondata',
                     'label': 'Feed -> Coupon Redemption'},
                    {'model': 'ascsaveform',
                     'label': 'Save Form -> ASC'},
                    {'model': 'auditlog', 'label': 'Audit Log'},
                    {'model': 'datafeedlog',
                     'label': 'Feed Log'}, 
                    {'model': 'customertempregistration',
                     'label': ' Customer registration'}, 'uploadproductcsv',
                    'messagetemplate', 'emailtemplate', 'gladmindusers',)},
        {'app': 'aftersell', 'label': 'AfterSell', 'icon': ' icon-folder-open',
         'models': ({'model': 'serviceadvisordealerrelationship', 'label': 'Feed -> Service Advisor'},
                    {'model': 'dispatchedproduct',
                     'label': 'Feed -> Product Dispatch'},
                    {'model': 'productdata',
                     'label': 'Feed -> Product Purchase'},
                    {'model': 'coupondata',
                     'label': 'Feed -> Coupon Redemption'},
                    {'model': 'ascsaveform',
                     'label': 'Save Form -> ASC'},
                    {'model': 'auditlog', 'label': 'Audit Log'},
                    {'model': 'datafeedlog',
                     'label': 'Feed Log'}, 'uploadproductcsv',
                    'messagetemplate', 'emailtemplate', 'gladmindusers',)},
        {'app': 'djcelery', 'label': 'Job Management', 'icon': 'icon-tasks'})
}


MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': 'gladminds.db',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        'PORT': '',                      # Set to empty string for default.
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
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'gladminds.middleware.GladmindsMessageMiddleware'
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

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'suit',
    'django.contrib.admin',
    'import_export',
    'gladminds.models',
    'gladminds.superadmin',
    'gladminds.afterbuy',
    'gladminds.aftersell',
    'gladminds',
    'djcelery',
    'corsheaders',
    'storages',
    'tastypie_swagger',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'provider',
    'provider.oauth2',
    'debug_toolbar',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

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
        'gladminds': {
            'handlers': ['gladminds_logs','console'],
            'level': 'INFO',
            'propagate': True,
        },
        'spyne': {
            'handlers': ['gladminds_logs','console'],
            'level': 'WARN',
            'propagate': True,
        }, 'afterbuy': {
            'handlers': ['afterbuy_logs','console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

WSDL_COUPON_REDEEM_LOC = TEMPLATE_DIR + '/coupon_redeem.wsdl'

WSDL_CUSTOMER_REGISTRATION_LOC = TEMPLATE_DIR + '/customer_registration.wsdl'

MAIL_SERVER = 'localhost'
MAIL_DETAIL = {
    "sender": "feed-report@gladminds.co",
    "receiver": ["gladminds@hashedin.com", "naveen.shankar@gladminds.co"],
    "subject": "Gladminds Feed Report",
    "body": """""",
}

FEED_FAILURE_MAIL_DETAIL = {

    "sender": "feed-report@gladminds.co",
    "receiver": ["gladminds+alerts@hashedin.com","support@gladminds.co"],
    "subject": "Gladminds Feed Failure Mail",
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
AWS_ACCESS_KEY_ID = 'AKIAIL7IDCSTNCG2R6JA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'afterbuy'
# S3_URL = 'http://%s.s3-website-us-east-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


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
AIRTEL_IP = '54.84.243.77'
SMS_CLIENT_DETAIL = { 'AIRTEL': {'login':'bajajauto',
                              'pass':'bajaj',
                              'authenticate_url':'http://117.99.128.32:80/login/pushsms.php',
                              'message_url': 'http://117.99.128.32:80/login/pushsms.php'},
                  'KAP': {'login':'GladMinds1',
                          'pass':'kap@user!23',
                          'message_url': 'http://alerts.kapsystem.com/api/web2sms.php',
                          'working_key': '1486415t035t8052c7pc',
                          'sender_id': 'GLADMS'}
                  }
