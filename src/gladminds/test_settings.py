# pylint: disable=W0401,W0614
from gladminds.settings import *
import os
import warnings
# added for removing warnings printed on console
import exceptions
warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning, module='django.db.models.fields', lineno=903)
warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning, module='django.db.models.fields', lineno=848)


OUT_DIR = os.path.join(BASE_DIR, "out")
DATA_CSV_PATH = os.path.join(BASE_DIR, "src/testdata")

DATABASES[GmApps.GM]['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES[GmApps.GM]['NAME'] = os.path.join(OUT_DIR, 'test.db')  # "/tmp/test.db"
DATABASES[GmApps.BAJAJ]['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES[GmApps.BAJAJ]['NAME'] = os.path.join(OUT_DIR, 'bajaj.db')  # "/tmp/test.db"
DATABASES[GmApps.DEMO]['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES[GmApps.DEMO]['NAME'] = os.path.join(OUT_DIR, 'demo.db')  # "/tmp/test.db"
DATABASES[GmApps.AFTERBUY]['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES[GmApps.AFTERBUY]['NAME'] = os.path.join(OUT_DIR, 'afterbuy.db')  # "/tmp/test.db"
DATABASES[GmApps.BAJAJCV]['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES[GmApps.BAJAJCV]['NAME'] = os.path.join(OUT_DIR, 'afterbuy.db')

TEST_IGNORE_APPS = ()

INSTALLED_APPS = ALL_APPS + TEST_IGNORE_APPS

SECRET_KEY = 'testsecretkeyshouldntbeusedinproduction'

INSTALLED_APPS = INSTALLED_APPS + ('django_nose',)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


SMS_CLIENT = "MOCK"
SMS_CLIENT_DETAIL = { 'AIRTEL': {'login':'mock',
                              'pass':'mock',
                              'authenticate_url':'',
                              'message_url': ''},
                  'KAP': {'login':'mock',
                              'pass':'mock',
                              'authenticate_url':'',
                              'message_url': '',
                              'params': 'KAP'},
                  'MOCK': {'login':'mock',
                              'pass':'mock',
                              'authenticate_url':'',
                              'message_url': ''}
                  }

BROKER_URL = 'redis://localhost:6379'
REDIS_URL = 'redis://localhost:6379'

FEED_TYPE = 'CSV'

LOGGING['handlers']['gladminds_logs']['filename'] = 'log/test_case.log'
LOGGING['handlers']['afterbuy_logs']['filename'] = 'log/test_case.log'
LOGGING['handlers']['sql']['filename'] = 'log/sql.log'
LOGGING['loggers']['gladminds']['handlers'] = ['gladminds_logs'] 
LOGGING['loggers']['spyne']['handlers'] = ['gladminds_logs'] 
LOGGING['loggers']['afterbuy']['handlers'] = ['afterbuy_logs'] 

FEED_FAILURE_MAIL_ENABLED = False

FEED_FAILURE_DIR = 'aftersell/{0}/feed-logs/dev/'
FEED_FAILURE_BUCKET = 'gladminds'
JOBCARD_DIR = '{0}/jobcards/dev/'

BRAND = 'bajaj'

ENV = "test"
MAIL_SERVER = 'localhost'

WSDL_TNS="http://local.bajaj.gladminds.co:8000/api/v1/feed/"

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
