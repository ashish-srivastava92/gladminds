from django.conf.urls import patterns, url, include
from django.conf import settings
from gladminds.core.cron_jobs.taskqueue import SqsHandler
from gladminds.sqs_tasks import _tasks_map


urlpatterns = patterns('',
    url(r'api/doc/', include('gladminds.core.api_docs.swagger_urls', namespace='tastypie_swagger')),
    
    url(r'^aftersell/users/(?P<users>[a-zA-Z0-9]+)$', 'gladminds.core.views.users'),
    url(r'^aftersell/sa/(?P<id>[a-zA-Z0-9]+)/$', 'gladminds.core.views.get_sa_under_asc'),
    url(r'^report/(?P<role>[a-zA-Z0-9.-]+)/$', 'gladminds.core.views.brand_details'),
    url(r'^aftersell/reports/reconciliation$', 'gladminds.core.views.reports'),
    url(r'^asc/report/$', 'gladminds.core.views.get_active_asc_report'),
     
    url(r'^aftersell/register/(?P<menu>[a-zA-Z0-9]+)$', 'gladminds.core.views.register'),
    url(r'^aftersell/exceptions/(?P<exception>[a-zA-Z0-9]+)$', 'gladminds.core.views.exceptions'),
    url(r'^aftersell/asc/self-register/$', 'gladminds.core.views.save_asc_registration'),
    
    url(r'^aftersell/(?P<provider>[a-zA-Z]+)/login/$', 'gladminds.core.views.auth_login', name='user_login'),
    url(r'^aftersell/provider/logout$', 'gladminds.core.views.user_logout', name='user_logout'),
    url(r'^aftersell/provider/redirect$', 'gladminds.core.views.redirect_user'),
    url(r'^aftersell/users/otp/generate$', 'gladminds.core.views.generate_otp', name='generate_otp'),
    url(r'^aftersell/users/otp/validate', 'gladminds.core.views.validate_otp', name='validate_otp'),
    url(r'^aftersell/users/otp/update_pass', 'gladminds.core.views.update_pass', name='update_pass'),
    url(r'^aftersell/provider/change-password$', 'gladminds.core.views.change_password', name='change_password'),

    # Tasks URL
    url(r'^welcome', 'gladminds.bajaj.services.loyalty.send_welcome_message', name='send_welcome_message'),
    url(r'^tasks-view/', 'gladminds.core.views.sqs_tasks_view'),
    url(r'^trigger-tasks', 'gladminds.core.views.trigger_sqs_tasks'),
    url(r'^tasks', SqsHandler.as_view(task_map=_tasks_map)),

)