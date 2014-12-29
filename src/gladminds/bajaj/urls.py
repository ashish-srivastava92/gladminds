from django.conf.urls import patterns, url, include
from django.conf import settings
from gladminds.bajaj.admin import brand_admin
from tastypie.api import Api
from gladminds.core import urls as core_urls
from gladminds.core.apis import preferences_apis
from gladminds.bajaj.apis import user_apis, product_apis, coupon_apis
from gladminds.core.managers.sms_handler import SMSResources

api_v1 = Api(api_name="v1")
# api_v1.register(audit_api.AuditResources())
# api_v1.register(user_apis.UserProfileResource())
api_v1.register(user_apis.DealerResources())
api_v1.register(user_apis.AuthorizedServiceCenterResources())
api_v1.register(user_apis.ServiceAdvisorResources())
api_v1.register(product_apis.ProductTypeDataResources())
api_v1.register(product_apis.ProductDataResources())
api_v1.register(coupon_apis.CouponDataResources())
api_v1.register(preferences_apis.UserPreferenceResource())
api_v1.register(preferences_apis.BrandPreferenceResource())

api_v1.register(SMSResources())

urlpatterns = patterns('',
    url(r'^sms/','gladminds.bajaj.services.coupons.feed_views.send_sms', name='send_sms'),
    url(r'', include(core_urls)),
    url(r'', include(brand_admin.urls)),
    url(r'', include(api_v1.urls)),
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'^aftersell/servicedesk/helpdesk$', 'gladminds.bajaj.services.service_desk.servicedesk_views.service_desk', name='service_desk'),
    url(r'^aftersell/servicedesk/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_servicedesk_tickets', name='get_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_servicedesk_tickets', name='modify_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/comments/(?P<comment_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_feedback_comments', name='modify_feedback_comments'),
    url(r'^aftersell/feedbackresponse/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_feedback_response', name='get_feedback_response'),
    url(r'^api/v1/mock-feed/$', 'gladminds.bajaj.feeds.webservice.mock_service'),
    url(r'^api/v1/mock-feed/\?wsdl$', 'gladminds.bajaj.feeds.webservice.mock_service'),
    url(r'^api/v1/feed/\?wsdl$', 'gladminds.bajaj.feeds.webservice.all_service'),
    url(r'^api/v1/feed/$', 'gladminds.bajaj.feeds.webservice.all_service'),
    url(r'^api/v1/brand-feed/\?wsdl$', 'gladminds.bajaj.feeds.webservice.brand_service'),
    url(r'^api/v1/brand-feed/$', 'gladminds.bajaj.feeds.webservice.brand_service'),
    url(r'^api/v1/dealer-feed/\?wsdl$', 'gladminds.bajaj.feeds.webservice.dealer_service'),
    url(r'^api/v1/dealer-feed/$', 'gladminds.bajaj.feeds.webservice.dealer_service'),
    url(r'^api/v1/dispatch-feed/\?wsdl$', 'gladminds.bajaj.feeds.webservice.dispatch_service'),
    url(r'^api/v1/dispatch-feed/$', 'gladminds.bajaj.feeds.webservice.dispatch_service'),
    url(r'^api/v1/purchase-feed/\?wsdl$', 'gladminds.bajaj.feeds.webservice.purchase_service'),
    url(r'^api/v1/purchase-feed/$', 'gladminds.bajaj.feeds.webservice.purchase_service'),
    url(r'^api/v1/asc-feed/\?wsdl$', 'gladminds.bajaj.feeds.webservice.asc_service'),
    url(r'^api/v1/asc-feed/$', 'gladminds.bajaj.feeds.webservice.asc_service'),
    url(r'^api/v1/bajaj/old-fsc-feed/\?wsdl$', 'gladminds.bajaj.feeds.webservice.old_fsc_service'),
    url(r'^api/v1/bajaj/old-fsc-feed/$', 'gladminds.bajaj.feeds.webservice.old_fsc_service'),
    url(r'^api/v1/bajaj/credit-note-feed/$', 'gladminds.bajaj.feeds.webservice.credit_note_service'), 
    url(r'^api/v1/redeem-feed/$', 'gladminds.bajaj.services.coupons.feed_views.views_coupon_redeem_wsdl', {'document_root': settings.WSDL_COUPON_REDEEM_LOC}),
    url(r'^api/v1/customer-feed/$', 'gladminds.bajaj.services.coupons.feed_views.views_customer_registration_wsdl', {'document_root': settings.WSDL_CUSTOMER_REGISTRATION_LOC}),
    url(r'^aftersell/users/(?P<users>[a-zA-Z0-9]+)$', 'gladminds.bajaj.views.views.users'),
    url(r'^aftersell/sa/(?P<id>[a-zA-Z0-9]+)/$', 'gladminds.bajaj.views.views.get_sa_under_asc'),
    url(r'^report/(?P<role>[a-zA-Z0-9.-]+)/$', 'gladminds.bajaj.views.views.brand_details'),
    url(r'^aftersell/reports/reconciliation$', 'gladminds.bajaj.views.views.reports'),
    url(r'^asc/report/$', 'gladminds.bajaj.views.views.get_active_asc_report'),
     
    url(r'^aftersell/register/(?P<menu>[a-zA-Z0-9]+)$', 'gladminds.bajaj.views.views.register'),
    url(r'^aftersell/exceptions/(?P<exception>[a-zA-Z0-9]+)$', 'gladminds.bajaj.views.views.exceptions'),
    url(r'^aftersell/asc/self-register/$', 'gladminds.bajaj.views.views.save_asc_registration'),
    
    url(r'^aftersell/(?P<provider>[a-zA-Z]+)/login/$', 'gladminds.bajaj.views.views.auth_login', name='user_login'),
    url(r'^aftersell/provider/logout$', 'gladminds.bajaj.views.views.user_logout', name='user_logout'),
    url(r'^aftersell/provider/redirect$', 'gladminds.bajaj.views.views.redirect_user'),
    url(r'^aftersell/users/otp/generate$', 'gladminds.bajaj.views.views.generate_otp', name='generate_otp'),
    url(r'^aftersell/users/otp/validate', 'gladminds.bajaj.views.views.validate_otp', name='validate_otp'),
    url(r'^aftersell/users/otp/update_pass', 'gladminds.bajaj.views.views.update_pass', name='update_pass'),
    url(r'^aftersell/provider/change-password$', 'gladminds.bajaj.views.views.change_password', name='change_password'),

    

)