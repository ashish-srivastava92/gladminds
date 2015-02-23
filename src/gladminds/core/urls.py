from django.conf.urls import patterns, url, include
from gladminds.core.cron_jobs.taskqueue import SqsHandler
from gladminds.sqs_tasks import _tasks_map

from tastypie.api import Api
from django.conf import settings
from gladminds.core.apis import user_apis, preferences_apis, coupon_apis, product_apis,\
    audit_apis, dashboard_apis, service_desk_apis
from gladminds.core.managers.sms_handler import SMSResources
from gladminds.core.apis.image_apis import upload_files

api_v1 = Api(api_name="v1")
api_v1.register(coupon_apis.CouponDataResource())
api_v1.register(product_apis.ProductTypeResource())
api_v1.register(product_apis.ProductResource())
api_v1.register(product_apis.CustomerTempRegistrationResource())
api_v1.register(user_apis.UserProfileResource())
api_v1.register(user_apis.DealerResource())
api_v1.register(user_apis.AuthorizedServiceCenterResource())
api_v1.register(user_apis.ServiceAdvisorResource())
api_v1.register(preferences_apis.UserPreferenceResource())
api_v1.register(preferences_apis.BrandPreferenceResource())
api_v1.register(audit_apis.SMSLogResource())
api_v1.register(audit_apis.DataFeedLogResource())
api_v1.register(dashboard_apis.OverallStatusResource())
api_v1.register(dashboard_apis.FeedStatusResource())
api_v1.register(dashboard_apis.SMSReportResource())
api_v1.register(dashboard_apis.CouponReportResource())
api_v1.register(service_desk_apis.ServiceDeskUserResource())
api_v1.register(service_desk_apis.FeedbackResource())

from django.contrib.auth.decorators import login_required
from django.contrib import admin
admin.autodiscover()
admin.site.login = login_required(settings.LOGIN_URL)

api_v1.register(SMSResources())

urlpatterns = patterns('',
    url(r'api/doc/', include('gladminds.core.api_docs.swagger_urls', namespace='tastypie_swagger')),
    url(r'login/$', 'gladminds.core.views.auth_login'),
    url(r'^$', 'gladminds.core.views.get_services'),
    (r'^admin/', include(admin.site.urls) ),
    url(r'^aftersell/users/(?P<users>[a-zA-Z0-9]+)$', 'gladminds.core.views.users'),
    url(r'^aftersell/sa/(?P<id>[a-zA-Z0-9]+)/$', 'gladminds.core.views.get_sa_under_asc'),
    url(r'^report/(?P<role>[a-zA-Z0-9.-]+)/$', 'gladminds.core.views.brand_details'),
    url(r'^aftersell/reports/reconciliation$', 'gladminds.core.views.reports'),
    url(r'^asc/report/$', 'gladminds.core.views.get_active_asc_report'),
    url(r'^aftersell/servicedesk/save-feedback/$', 'gladminds.core.services.service_desk.servicedesk_views.save_feedback', name='save_feedback'),
    
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

    url(r'^aftersell/servicedesk/helpdesk$', 'gladminds.core.services.service_desk.servicedesk_views.service_desk', name='enable_servicedesk'),
    url(r'^aftersell/servicedesk/$', 'gladminds.core.services.service_desk.servicedesk_views.get_servicedesk_tickets', name='get_servicedesk_tickets'),
    url(r'^aftersell/helpdesk$', 'gladminds.core.services.service_desk.servicedesk_views.get_helpdesk', name='get_helpdesk'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/$', 'gladminds.core.services.service_desk.servicedesk_views.modify_servicedesk_tickets', name='modify_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/comments/(?P<comment_id>\d+)/$', 'gladminds.core.services.service_desk.servicedesk_views.modify_feedback_comments', name='modify_feedback_comments'),
    url(r'^aftersell/feedbackresponse/(?P<feedback_id>\d+)/$', 'gladminds.core.services.service_desk.servicedesk_views.get_feedback_response', name='get_feedback_response'),
    url(r'^aftersell/servicedesk/save-feedback/$', 'gladminds.core.services.service_desk.servicedesk_views.save_feedback', name='save_feedback'),

    url(r'^v1/upload', upload_files),
    # Tasks URL
    url(r'^tasks-view/', 'gladminds.core.views.sqs_tasks_view'),
    url(r'^trigger-tasks', 'gladminds.core.views.trigger_sqs_tasks'),
    url(r'^tasks', SqsHandler.as_view(task_map=_tasks_map)),

)