from django.conf.urls import patterns, url, include
from gladminds.bajaj.admin import brand_admin
from gladminds.core import urls as core_urls
from gladminds.core.apis import user_apis 
from gladminds.core.urls import api_v1
from gladminds.bajaj.services.loyalty.loyalty import LoyaltyService
from tastypie.api import Api
from gladminds.core.apis import loyalty_apis, product_apis

loyalty = LoyaltyService

loyalty_v1 = Api(api_name="loyalty/v1")
loyalty_v1.register(user_apis.UserResource())
loyalty_v1.register(user_apis.UserProfileResource())
loyalty_v1.register(loyalty_apis.NSMResource())
loyalty_v1.register(loyalty_apis.ASMResource())
loyalty_v1.register(loyalty_apis.PartnerResource())
loyalty_v1.register(loyalty_apis.DistributorResource())
loyalty_v1.register(loyalty_apis.RetailerResource())
loyalty_v1.register(product_apis.ProductTypeResource())
loyalty_v1.register(loyalty_apis.SpareMasterResource())
loyalty_v1.register(loyalty_apis.RedemptionResource())
loyalty_v1.register(loyalty_apis.ProductResource())
loyalty_v1.register(loyalty_apis.SparePartUPCResource())
loyalty_v1.register(loyalty_apis.SparePartPointResource())
loyalty_v1.register(loyalty_apis.LoyaltySLAResource())
loyalty_v1.register(loyalty_apis.MemberResource())
loyalty_v1.register(loyalty_apis.AccumulationResource())
loyalty_v1.register(loyalty_apis.CommentThreadResource())
loyalty_v1.register(loyalty_apis.WelcomeKitResource())
loyalty_v1.register(loyalty_apis.DiscrepantAccumulationResource())
loyalty_v1.register(loyalty_apis.TerritoryResource())
loyalty_v1.register(loyalty_apis.StateResource())
loyalty_v1.register(loyalty_apis.CityResource())


urlpatterns = patterns('',
    url(r'^sms/','gladminds.bajaj.services.feed_views.send_sms', name='send_sms'),
    url(r'', include(brand_admin.urls)),
    url(r'', include(api_v1.urls)),
    url(r'', include(loyalty_v1.urls)),
    url(r'^site-info-hackish/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'^aftersell/servicedesk/helpdesk$', 'gladminds.bajaj.services.service_desk.servicedesk_views.service_desk', name='enable_servicedesk'),
    url(r'^aftersell/servicedesk/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_servicedesk_tickets', name='get_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_servicedesk_tickets', name='modify_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/comments/(?P<comment_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_feedback_comments', name='modify_feedback_comments'),
    url(r'^aftersell/feedbackresponse/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_feedback_response', name='get_feedback_response'),
    url(r'^aftersell/servicedesk/save-feedback/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.save_feedback', name='save_feedback'),
    
    url(r'^api/v1/feed/\?wsdl$', 'gladminds.bajaj.webservice.all_service'),
    url(r'^api/v1/feed/$', 'gladminds.bajaj.webservice.all_service'),

    url(r'^api/v1/redeem-feed/$', 'gladminds.bajaj.services.feed_views.views_coupon_redeem_wsdl'),
    url(r'^api/v1/customer-feed/$', 'gladminds.bajaj.services.feed_views.views_customer_registration_wsdl'),
    url(r'^api/v1/vin-sync-feed/$', 'gladminds.bajaj.services.feed_views.views_vin_sync_wsdl'),
    url(r'^api/v1/member-sync-feed/$', 'gladminds.bajaj.services.feed_views.views_member_sync_wsdl'),
    url(r'^api/v1/purchase-sync-feed/$', 'gladminds.bajaj.services.feed_views.views_purchase_sync_wsdl'),

    url(r'^aftersell/users/(?P<users>[a-zA-Z0-9]+)$', 'gladminds.bajaj.views.views.users'),
    url(r'^aftersell/sa/(?P<id>[a-zA-Z0-9]+)/$', 'gladminds.bajaj.views.views.get_sa_under_asc'),
    url(r'^report/(?P<role>[a-zA-Z0-9.-]+)/$', 'gladminds.bajaj.views.views.brand_details'),
    url(r'^aftersell/reports/reconciliation$', 'gladminds.bajaj.views.views.reports'),
    url(r'^coupon/report/(?P<role>[a-zA-Z0-9.-]+)/$', 'gladminds.bajaj.views.views.get_active_asc_report'),
    url(r'^aftersell/register/(?P<menu>[a-zA-Z0-9]+)$', 'gladminds.bajaj.views.views.register'),
    url(r'^aftersell/exceptions/(?P<exception>[a-zA-Z0-9]+)$', 'gladminds.bajaj.views.views.exceptions'),
    url(r'^aftersell/feeds/vin-sync/$', 'gladminds.bajaj.views.views.vin_sync_feed'),
    url(r'^aftersell/asc/self-register/$', 'gladminds.bajaj.views.views.save_asc_registration'),
    
    url(r'^update-customer-number$', 'gladminds.bajaj.services.service_desk.servicedesk_views.update_customer_number'),
    
    url(r'^aftersell/(?P<provider>[a-zA-Z]+)/login/$', 'gladminds.bajaj.views.views.auth_login', name='user_login'),
    url(r'^aftersell/provider/logout$', 'gladminds.bajaj.views.views.user_logout', name='user_logout'),
    url(r'^aftersell/provider/redirect$', 'gladminds.bajaj.views.views.redirect_user'),
    url(r'^aftersell/users/otp/generate$', 'gladminds.bajaj.views.views.generate_otp', name='generate_otp'),
    url(r'^aftersell/users/otp/validate', 'gladminds.bajaj.views.views.validate_otp', name='validate_otp'),
    url(r'^aftersell/users/otp/update_pass', 'gladminds.bajaj.views.views.update_pass', name='update_pass'),
    url(r'^aftersell/provider/change-password$', 'gladminds.bajaj.views.views.change_password', name='change_password'),
    
    url(r'^aftersell/servicedesk/helpdesk$', 'gladminds.bajaj.services.service_desk.servicedesk_views.service_desk', name='service_desk'),
    url(r'^aftersell/servicedesk/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_servicedesk_tickets', name='get_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_servicedesk_tickets', name='modify_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/comments/(?P<comment_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_feedback_comments', name='modify_feedback_comments'),
    url(r'^aftersell/feedbackresponse/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_feedback_response', name='get_feedback_response'),
    url(r'^welcome', loyalty.send_welcome_message, name='send_welcome_message'),
    url(r'^kit/download/(?P<choice>[a-zA-Z0-9]+)$', loyalty.download_welcome_kit, name='download_welcome_kit'),
    url(r'', include(core_urls)),
)