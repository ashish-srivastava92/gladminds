from django.conf.urls import patterns, url, include
from gladminds.bajaj.admin import brand_admin
from gladminds.core import urls as core_urls
from gladminds.core.urls import api_v1

urlpatterns = patterns('',
    #api urls
    # url(r'^mc/api-token-auth/', 'gladminds.bajaj.views.apis.authentication'),
    # 
    
    url(r'^mc/api-token-auth/', 'gladminds.bajaj.views.apis.authentication'),
    url(r'^mc/get_retailers/dsr_id/(?P<dsr_id>\d+)/$', 'gladminds.bajaj.views.apis.get_retailers'),
    url(r'^mc/get_retailer_profile/retailer_id/(?P<retailer_id>\d+)/$',
                                                'gladminds.bajaj.views.apis.get_retailer_profile'),
    
    url(r'^mc/get_parts/', 'gladminds.bajaj.views.apis.get_parts'),
    
    #url(r'^mc/place_order/dsr_id/(?P<dsr_id>\d+)$', 'gladminds.bajaj.views.apis.place_order'),
    
    url(r'^mc/order/$', 'gladminds.core.views.apis.retailer_order'),
    
    url(r'^mc/day_close_order/dsr_id/(?P<dsr_id>\d+)/$',
                        'gladminds.bajaj.views.apis.day_close_order'),
    
    
    url(r'^mc/get_outstanding/dsr_id/(?P<dsr_id>\d+)/$',
                        'gladminds.bajaj.views.apis.get_outstanding'),
    
    url(r'^mc/get_collection/dsr_id/(?P<dsr_id>\d+)$',
                        'gladminds.bajaj.views.apis.get_collection'),
    
    url(r'^mc/get_distributor_for_retailer/retailer_id/(?P<retailer_id>\d+)/$',
                        'gladminds.bajaj.views.apis.get_distributor_for_retailer'),
    
    url(r'^mc/get_outstanding/dsr_id/(?P<retailer_id>\d+)/$',
                        'gladminds.bajaj.views.apis.get_outstanding'),
    url(r'^mc/get_schedule/dsr_id/(?P<dsr_id>\d+)/date/(?P<date>[-\d]+)/$',
                        'gladminds.bajaj.views.apis.get_schedule'),
    url(r'^mc/place_order/dsr_id/(?P<dsr_id>\d+)$',
                        'gladminds.bajaj.views.apis.place_order'),
    
    
    #end of api urls
    
    url(r'^bulk_upload_retailer/$', 'gladminds.bajaj.views.views.bulk_upload_retailer', name='bulk_upload_retailer'),
    
    url(r'^sms/','gladminds.bajaj.services.feed_views.send_sms', name='send_sms'),
    url(r'^admin/', include(brand_admin.urls)),
    url(r'', include(api_v1.urls)),
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'^aftersell/servicedesk/helpdesk$', 'gladminds.bajaj.services.service_desk.servicedesk_views.service_desk', name='enable_servicedesk'),
    url(r'^aftersell/servicedesk/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_servicedesk_tickets', name='get_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_servicedesk_tickets', name='modify_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/comments/(?P<comment_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_feedback_comments', name='modify_feedback_comments'),
    url(r'^aftersell/feedbackresponse/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_feedback_response', name='get_feedback_response'),
    url(r'^aftersell/servicedesk/save-feedback/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.save_feedback', name='save_feedback'),
    
    url(r'^api/v1/feed/\?wsdl$', 'gladminds.bajaj.webservice.all_service'),
    url(r'^api/v1/feed/$', 'gladminds.bajaj.webservice.all_service'),

    url(r'^api/v1/(?P<feed_type>[a-zA-Z0-9-]+)/$', 'gladminds.bajaj.services.feed_views.view_wsdl'),

    url(r'^aftersell/users/(?P<users>[a-zA-Z0-9]+)$', 'gladminds.bajaj.views.views.users'),
    url(r'^aftersell/sa/(?P<id>[a-zA-Z0-9]+)/$', 'gladminds.bajaj.views.views.get_sa_under_asc'),
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
    url(r'^admin/retailer/rejected_reason$', 'gladminds.bajaj.views.views.rejected_reason', name='rejected_reason'),
        
    url(r'^aftersell/servicedesk/helpdesk$', 'gladminds.bajaj.services.service_desk.servicedesk_views.service_desk', name='service_desk'),
    url(r'^aftersell/servicedesk/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_servicedesk_tickets', name='get_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_servicedesk_tickets', name='modify_servicedesk_tickets'),
    url(r'^aftersell/feedbackdetails/(?P<feedback_id>\d+)/comments/(?P<comment_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.modify_feedback_comments', name='modify_feedback_comments'),
    url(r'^aftersell/feedbackresponse/(?P<feedback_id>\d+)/$', 'gladminds.bajaj.services.service_desk.servicedesk_views.get_feedback_response', name='get_feedback_response'),
    url(r'', include(core_urls)),
    url(r'^get_user_info/$', 'gladminds.bajaj.views.views.get_user_info', name='get_user_info'),
    url(r'^get_districts/$', 'gladminds.bajaj.views.views.get_districts', name='get_districts'),
    url(r'^save_order_history/$', 'gladminds.bajaj.views.views.save_order_history', name='save_order_history'),
    
    url(r'^ordered_part_details/(?P<part_number>\w+)/$', 'gladminds.bajaj.views.views.ordered_part_details', name='ordered_part_details'),
    
    
    url(r'^admin/retailer/approve_retailer/retailer_id/(?P<retailer_id>\d+)/$', 'gladminds.bajaj.views.views.approve_retailer', name='approve_retailer'),
#     url(r'^admin/bajaj/view_orders/(?P<order_id>\d+)$', 'gladminds.bajaj.views.views.list_orders', name='list_orders'),
)