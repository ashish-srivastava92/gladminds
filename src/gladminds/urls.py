from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api
from gladminds.resource import resources as r 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

api_v1 = Api(api_name="v1")
api_v1.register(r.GladmindsResources())
api_v1.register(r.BrandResources())
api_v1.register(r.ProductTypeResources())
api_v1.register(r.ProductResources())
api_v1.register(r.UserResources())

urlpatterns = patterns('',
  url(r'^dealers/$', 'django.contrib.auth.views.login', {'template_name': 'dealer/login.html'}),
  url(r'^dealers/logout$', 'django.contrib.auth.views.logout', {'template_name': 'dealer/logout.html'}),
)

urlpatterns += patterns('gladminds',
    (r'', include(api_v1.urls)),
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
    url(r'^api/v1/bajaj/redeem-feed/$', 'superadmin.views.views_coupon_redeem_wsdl', {'document_root': settings.WSDL_COUPON_REDEEM_LOC}),
    
    url(r'^app/logout', 'afterbuy.views.app_logout', name='app_logout'),
    url(r'^app', 'afterbuy.views.home', name='home'),
    url(r'^gm', 'afterbuy.views.main', name='main'),
    
    # Examples:
#     url(r'^app/create-account', 'afterbuy.views.create_account', name='create_account'),
#     url(r'^app/login', 'afterbuy.views.my_login', name='my_login'),
#     url(r'^app/getData', 'afterbuy.views.get_data', name='get_data'),
    # url(r'^$', 'gladminds.views.home', name='home'),
    # url(r'^gladminds/', include('gladminds.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^sms/','superadmin.views.send_sms', name='send_sms'),
    url(r'^dealers/([a-zA-Z0-9]+)', 'views.action', name='actions'),
    url(r'^', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
