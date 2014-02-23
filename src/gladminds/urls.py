from django.conf.urls import patterns, include, url
from tastypie.api import Api
from gladminds.resource import resources as r 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

api_v1 = Api(api_name="v1")
api_v1.register(r.GladmindsResources())

urlpatterns = patterns('gladminds',
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
    url(r'^api/v1/bajaj/redeem-feed/$', 'webservice.coupon_redeem_service'),
    url(r'^app', 'afterbuy.views.home', name='home'),
    # Examples:
    # url(r'^$', 'gladminds.views.home', name='home'),
    # url(r'^gladminds/', include('gladminds.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^sms/','superadmin.views.send_sms', name='send_sms'),
    url(r'^', include(admin.site.urls)),
)
