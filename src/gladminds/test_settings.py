# pylint: disable=W0401,W0614
from settings import *
import os

OUT_DIR = os.path.join(BASE_DIR, "out")
DATA_CSV_PATH = os.path.join(BASE_DIR, "src/testdata")

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = os.path.join(OUT_DIR, 'test.db')#"/tmp/test.db"
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
        'gladminds_logs': {
            'level': 'INFO',
            'filename': '/var/log/gladminds/app/test_case.log',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
        },
        'afterbuy_logs': {
            'level': 'INFO',
            'filename': '/var/log/gladminds/app/test_case.log',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },'gladminds': {
            'handlers': ['gladminds_logs'],
            'level': 'DEBUG',
            'propagate': True,
        },'spyne': {
            'handlers': ['gladminds_logs'],
            'level': 'DEBUG',
            'propagate': False,
        },'afterbuy': {
            'handlers': ['afterbuy_logs'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
