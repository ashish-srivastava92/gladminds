from django.conf.urls import patterns, url, include
from django.conf import settings
from gladminds.bajaj.admin import brand_admin
from gladminds.core import urls as core_urls


urlpatterns = patterns('',
    url(r'^', include(core_urls)),
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'^', include(brand_admin.urls)),
    url(r'^api/v1/mock-feed/$', 'gladminds.core.webservice.mock_service'),
    url(r'^api/v1/mock-feed/\?wsdl$', 'gladminds.core.webservice.mock_service'),
    url(r'^api/v1/feed/\?wsdl$', 'gladminds.core.webservice.all_service'),
    url(r'^api/v1/feed/$', 'gladminds.core.webservice.all_service'),
    url(r'^api/v1/brand-feed/\?wsdl$', 'gladminds.core.webservice.brand_service'),
    url(r'^api/v1/brand-feed/$', 'gladminds.core.webservice.brand_service'),
    url(r'^api/v1/dealer-feed/\?wsdl$', 'gladminds.core.webservice.dealer_service'),
    url(r'^api/v1/dealer-feed/$', 'gladminds.core.webservice.dealer_service'),
    url(r'^api/v1/dispatch-feed/\?wsdl$', 'gladminds.core.webservice.dispatch_service'),
    url(r'^api/v1/dispatch-feed/$', 'gladminds.core.webservice.dispatch_service'),
    url(r'^api/v1/purchase-feed/\?wsdl$', 'gladminds.core.webservice.purchase_service'),
    url(r'^api/v1/purchase-feed/$', 'gladminds.core.webservice.purchase_service'),
    url(r'^api/v1/asc-feed/\?wsdl$', 'gladminds.core.webservice.asc_service'),
    url(r'^api/v1/asc-feed/$', 'gladminds.core.webservice.asc_service'),    
    url(r'^api/v1/redeem-feed/$', 'gladminds.superadmin.views.views_coupon_redeem_wsdl', {'document_root': settings.WSDL_COUPON_REDEEM_LOC}),
    url(r'^api/v1/customer-feed/$', 'gladminds.superadmin.views.views_customer_registration_wsdl', {'document_root': settings.WSDL_CUSTOMER_REGISTRATION_LOC}),
    
    url(r'^aftersell/register/(?P<menu>[a-zA-Z0-9]+)$', 'gladminds.views.register'),
    url(r'^aftersell/exceptions/(?P<exception>[a-zA-Z0-9]+)$', 'gladminds.views.exceptions'),
    url(r'^aftersell/reports/(?P<report>[a-zA-Z0-9]+)$', 'gladminds.views.reports'),
    url(r'^aftersell/asc/self-register/$', 'gladminds.views.asc_registration'),
    
        
    url(r'^aftersell/(?P<provider>[a-zA-Z]+)/login/$', 'gladminds.views.auth_login', name='user_login'),
    url(r'^aftersell/provider/logout$', 'gladminds.views.user_logout', name='user_logout'),
    url(r'^aftersell/provider/redirect$', 'gladminds.views.redirect_user'),
    url(r'^aftersell/users/otp/generate$', 'gladminds.views.generate_otp', name='generate_otp'),
    url(r'^aftersell/users/otp/validate', 'gladminds.views.validate_otp', name='validate_otp'),
    url(r'^aftersell/users/otp/update_pass', 'gladminds.views.update_pass', name='update_pass'),
    
    url(r'^aftersell/servicedesk/(?P<servicedesk>[a-zA-Z0-9]+)$', 'gladminds.views.servicedesk'),
    url(r'^aftersell/servicedesk/$', 'gladminds.views.servicedesk_views.get_servicedesk_tickets', name='get_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/$', 'gladminds.views.servicedesk_views.modify_servicedesk_tickets', name='modify_servicedesk_tickets'),
    url(r'^aftersell/feedbackresponse/(?P<feedback_id>\d+)/$', 'gladminds.views.servicedesk_views.get_feedback_response', name='get_feedback_response'),

)