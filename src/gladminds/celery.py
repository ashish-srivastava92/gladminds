from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gladminds.dev_settings')

app = Celery('gladminds')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.CELERY_TIMEZONE = 'UTC'
app.conf.CELERYBEAT_SCHEDULE= {
    # Send a reminder message to customer on service coupon expiry.
    'cronjob-send-reminder-daily-midnight': {
        'task': 'gladminds.tasks.send_reminder',
        'schedule': crontab(minute=0, hour=0),
        'kwargs': {'reminder_day':7}
    },
    
    # Import data from SAP CRM to MySQL
    'cronjob-import_sap_data_to_db': {
        'task': 'gladminds.tasks.import_data',
        'schedule': crontab(minute=0, hour=0),
    },
    
    #Job to send reminder message schedule by admin
    'cronjob-reminder_message_schedule_by_admin': {
        'task': 'gladminds.tasks.send_schedule_reminder',
        'schedule': crontab(minute=0, hour=0),
    },
                               
    #Job to set expire status=True for all service coupon which expire 
    'cronjob-set-expiry-status-to-service-coupon': {
        'task': 'gladminds.tasks.expire_service_coupon',
        'schedule': crontab(minute=0, hour=0),
    },  
    #Job to set expire status=True for all service coupon which expire 
    'cronjob-export-csv-file': {
        'task': 'gladminds.tasks.export_close_coupon_data',
        'schedule': crontab(minute=0, hour=0),
    },                                     
}
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    
