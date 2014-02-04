# pylint: disable=W0401,W0614
from settings import *
import os

OUT_DIR = os.path.join(BASE_DIR, "out")
DATA_CSV_PATH = os.path.join(BASE_DIR, "src/testdata")

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = os.path.join(OUT_DIR, 'test.db')
SECRET_KEY = 'testsecretkeyshouldntbeusedinproduction'

INSTALLED_APPS = INSTALLED_APPS + ('django_nose',)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SMS_CLIENT = "MOCK"

SMS_CLIENT_DETAIL = {
                     'OTP_TWILIO_ACCOUNT' : 'MOCK_ACCOUNT',
                     'OTP_TWILIO_AUTH' : 'MOCK_AUTH',
                     'OTP_TWILIO_FROM' : 'MOCK_PHONE',
                     'OTP_TWILIO_URI' : 'MOCK_URI'
            }

BROKER_URL= 'redis://localhost:6379'
REDIS_URL = 'redis://localhost:6379'

FEED_TYPE='CSV'


