from django.conf.urls import patterns, url, include
from django.conf import settings
from gladminds.bajaj.admin import brand_admin
from gladminds.bajaj.feeds import webservice


urlpatterns = patterns('',
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'', include(brand_admin.urls)),
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
    url(r'^api/v1/bajaj/old-fsc-feed/\?wsdl$', 'webservice.old_fsc_service'),
    url(r'^api/v1/bajaj/old-fsc-feed/$', 'webservice.old_fsc_service'),
    url(r'^api/v1/bajaj/credit-note-feed/$', 'webservice.credit_note_service'), 
    url(r'^api/v1/redeem-feed/$', 'gladminds.bajaj.services.feed_views.views_coupon_redeem_wsdl', {'document_root': settings.WSDL_COUPON_REDEEM_LOC}),
    url(r'^api/v1/customer-feed/$', 'gladminds.bajaj.services.feed_views.views_customer_registration_wsdl', {'document_root': settings.WSDL_CUSTOMER_REGISTRATION_LOC}),

    url(r'^aftersell/users/(?P<users>[a-zA-Z0-9]+)$', 'gladminds.core.views.users'),
    url(r'^aftersell/sa/(?P<id>[a-zA-Z0-9]+)/$', 'gladminds.core.views.get_sa_under_asc'),
    url(r'^aftersell/(?P<role>[a-zA-Z0-9.-]+)/$', 'gladminds.core.views.brand_details'),
    url(r'^aftersell/reports/reconciliation$', 'gladminds.core.views.reports'),
     
    url(r'^aftersell/register/(?P<menu>[a-zA-Z0-9]+)$', 'gladminds.core.views.register'),
    url(r'^aftersell/exceptions/(?P<exception>[a-zA-Z0-9]+)$', 'gladminds.core.views.exceptions'),
    url(r'^aftersell/asc/self-register/$', 'gladminds.core.views.asc_registration'),
    
    url(r'^aftersell/(?P<provider>[a-zA-Z]+)/login/$', 'gladminds.core.views.auth_login', name='user_login'),
    url(r'^aftersell/provider/logout$', 'gladminds.core.views.user_logout', name='user_logout'),
    url(r'^aftersell/provider/redirect$', 'gladminds.core.views.redirect_user'),
    url(r'^aftersell/users/otp/generate$', 'gladminds.core.views.generate_otp', name='generate_otp'),
    url(r'^aftersell/users/otp/validate', 'gladminds.core.views.validate_otp', name='validate_otp'),
    url(r'^aftersell/users/otp/update_pass', 'gladminds.core.views.update_pass', name='update_pass'),
    url(r'^aftersell/provider/change-password$', 'gladminds.views.change_password', name='change_password'),
    
    url(r'^aftersell/servicedesk/(?P<servicedesk>[a-zA-Z0-9]+)$', 'gladminds.core.views.servicedesk'),
    url(r'^aftersell/servicedesk/$', 'gladminds.bajaj.services.service_desk.get_servicedesk_tickets', name='get_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.modify_servicedesk_tickets', name='modify_servicedesk_tickets'),
    url(r'^aftersell/feedbackresponse/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.get_feedback_response', name='get_feedback_response'),
)