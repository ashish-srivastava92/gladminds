from dev_settings import *

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