from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api
from gladminds.resource import resources
from gladminds.sqs_tasks import _tasks_map
from gladminds.taskqueue import SqsHandler
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

api_v1 = Api(api_name="v1")
api_v1.register(resources.GladmindsResources())
api_v1.register(resources.BrandResources())
api_v1.register(resources.ProductTypeResources())
api_v1.register(resources.ProductResources())
api_v1.register(resources.UserResources())

urlpatterns = patterns('',
    url(r'^aftersell/(?P<provider>[a-zA-Z]+)/login/$', 'gladminds.views.auth_login', name='user_login'),
    url(r'^aftersell/provider/logout$', 'gladminds.views.user_logout', name='user_logout'),
    url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    url(r'^aftersell/provider/redirect$', 'gladminds.views.redirect_user'),

    url(r'^aftersell/register/(?P<menu>[a-zA-Z0-9]+)$', 'gladminds.views.register'),
    url(r'^aftersell/exceptions/(?P<exception>[a-zA-Z0-9]+)$', 'gladminds.views.exceptions'),
    url(r'^aftersell/users/otp/generate$', 'gladminds.views.generate_otp', name='generate_otp'),
    url(r'^aftersell/users/otp/validate', 'gladminds.views.validate_otp', name='validate_otp'),
    url(r'^aftersell/users/otp/update_pass', 'gladminds.views.update_pass', name='update_pass'),

    url(r'^aftersell/asc/self-register/$', 'gladminds.views.asc_registration'),

    #Afterbuy accesstoken URL.
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),

)

urlpatterns += patterns('gladminds',
    (r'', include(api_v1.urls)),
    url(r'^api/v1/bajaj/mock-feed/$', 'webservice.mock_service'),
    url(r'^api/v1/bajaj/mock-feed/\?wsdl$', 'webservice.mock_service'),
    url(r'^api/v1/bajaj/feed/\?wsdl$', 'webservice.all_service'),
    url(r'^api/v1/bajaj/feed/$', 'webservice.all_service'),
    url(r'^api/v1/bajaj/brand-feed/\?wsdl$', 'webservice.brand_service'),
    url(r'^api/v1/bajaj/brand-feed/$', 'webservice.brand_service'),
    url(r'^api/v1/bajaj/dealer-feed/\?wsdl$', 'webservice.dealer_service'),
    url(r'^api/v1/bajaj/dealer-feed/$', 'webservice.dealer_service'),
    url(r'^api/v1/bajaj/dispatch-feed/\?wsdl$', 'webservice.dispatch_service'),
    url(r'^api/v1/bajaj/dispatch-feed/$', 'webservice.dispatch_service'),
    url(r'^api/v1/bajaj/purchase-feed/\?wsdl$', 'webservice.purchase_service'),
    url(r'^api/v1/bajaj/purchase-feed/$', 'webservice.purchase_service'),
    url(r'^api/v1/bajaj/asc-feed/\?wsdl$', 'webservice.asc_service'),
    url(r'^api/v1/bajaj/asc-feed/$', 'webservice.asc_service'),    
    url(r'^api/v1/bajaj/redeem-feed/$', 'superadmin.views.views_coupon_redeem_wsdl', {'document_root': settings.WSDL_COUPON_REDEEM_LOC}),

    url(r'^app/logout', 'afterbuy.views.app_logout', name='app_logout'),
    url(r'^app', 'afterbuy.views.home', name='home'),
    
    
    # After buy API
    url(r'^afterbuy/product/coupons/$', 'afterbuy.api.get_product_coupons', name='get_product_coupons'),
    url(r'^afterbuy/product/purchase-info/$', 'afterbuy.api.get_product_purchase_information', name='get_product_purchase_information'),
    url(r'^afterbuy/product/warranty/$', 'afterbuy.api.get_product_warranty', name='get_product_warranty'),
    url(r'^afterbuy/product/insurance/$', 'afterbuy.api.get_product_insurance', name='get_product_insurance'),
    url(r'^afterbuy/product/info/$', 'afterbuy.api.get_user_product_information', name='get_user_product_information'),
    
    url(r'^afterbuy/otp/generate/', 'afterbuy.views.generate_otp'),
    url(r'^afterbuy/otp/validate/', 'afterbuy.views.validate_otp'),
    url(r'^v1/api/users/auth', 'afterbuy.views.get_access_token'),
    url(r'^tasks-view', 'views.sqs_tasks_view'),
    url(r'^trigger-tasks', 'views.trigger_sqs_tasks'),
    url(r'^tasks/', SqsHandler.as_view(task_map=_tasks_map)),

    url(r'^afterbuy/$', 'afterbuy.views.main', name='main'),
#     url(r'^app/create-account', 'afterbuy.views.create_account', name='create_account'),
#     url(r'^app/login', 'afterbuy.views.my_login', name='my_login'),
#     url(r'^app/getData', 'afterbuy.views.get_data', name='get_data'),
    # url(r'^$', 'gladminds.views.home', name='home'),
    # url(r'^gladminds/', include('gladminds.foo.urls')),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^sms/','superadmin.views.send_sms', name='send_sms'),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
