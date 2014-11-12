# pylint: disable=W0401,W0614
from gladminds.settings import *
import os

OUT_DIR = os.path.join(BASE_DIR, "out")
DATA_CSV_PATH = os.path.join(BASE_DIR, "src/testdata")

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = os.path.join(OUT_DIR, 'test.db')  # "/tmp/test.db"
SECRET_KEY = 'testsecretkeyshouldntbeusedinproduction'

INSTALLED_APPS = INSTALLED_APPS + ('django_nose',)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SMS_CLIENT = "AIRTEL"
SMS_CLIENT_DETAIL = {'login':'bajajauto',
                     'pass':'bajaj',
                     'authenticate_url':'http://117.99.128.32:80/login/pushsms.php',
                     'message_url': 'http://117.99.128.32:80/login/pushsms.php'}
BROKER_URL = 'redis://localhost:6379'
REDIS_URL = 'redis://localhost:6379'

FEED_TYPE = 'CSV'

LOGGING['handlers']['gladminds_logs']['filename'] = 'log/gladminds/app/test_case.log'
LOGGING['handlers']['afterbuy_logs']['filename'] = 'log/gladminds/app/test_case.log'

FEED_FAILURE_MAIL_ENABLED = False

FEED_FAILURE_DIR = 'aftersell/{0}/feed-logs/dev/'
FEED_FAILURE_BUCKET = 'gladminds'
JOBCARD_DIR = '{0}/jobcards/dev/'
