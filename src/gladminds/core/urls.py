from django.conf.urls import patterns, url, include
from gladminds.core.cron_jobs.taskqueue import SqsHandler
from gladminds.sqs_tasks import _tasks_map

from tastypie.api import Api
from gladminds.core.apis import user_apis, preferences_apis, coupon_apis, product_apis,\
    audit_apis, dashboard_apis
from gladminds.core.managers.sms_handler import SMSResources

api_v1 = Api(api_name="v1")
api_v1.register(coupon_apis.CouponDataResources())
api_v1.register(product_apis.ProductTypeResource())
api_v1.register(product_apis.ProductResource())
api_v1.register(user_apis.UserProfileResource())
api_v1.register(user_apis.DealerResources())
api_v1.register(user_apis.AuthorizedServiceCenterResources())
api_v1.register(user_apis.ServiceAdvisorResources())
api_v1.register(preferences_apis.UserPreferenceResource())
api_v1.register(preferences_apis.BrandPreferenceResource())
api_v1.register(audit_apis.SMSLogResource())
api_v1.register(dashboard_apis.OverallStatusResource())

api_v1.register(SMSResources())

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
    url(r'^aftersell/servicedesk/helpdesk$', 'gladminds.core.services.service_desk.servicedesk_views.service_desk', name='service_desk'),
    url(r'^aftersell/servicedesk/$', 'gladminds.core.services.service_desk.servicedesk_views.get_servicedesk_tickets', name='get_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/$', 'gladminds.core.services.service_desk.servicedesk_views.modify_servicedesk_tickets', name='modify_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/comments/(?P<comment_id>\d+)/$', 'gladminds.core.services.service_desk.servicedesk_views.modify_feedback_comments', name='modify_feedback_comments'),
    url(r'^aftersell/feedbackresponse/(?P<feedback_id>\d+)/$', 'gladminds.core.services.service_desk.servicedesk_views.get_feedback_response', name='get_feedback_response'),
    
    # Tasks URL
    url(r'^welcome', 'gladminds.bajaj.services.loyalty.loyalty.send_welcome_message', name='send_welcome_message'),
    url(r'^tasks-view/', 'gladminds.core.views.sqs_tasks_view'),
    url(r'^trigger-tasks', 'gladminds.core.views.trigger_sqs_tasks'),
    url(r'^tasks', SqsHandler.as_view(task_map=_tasks_map)),

)