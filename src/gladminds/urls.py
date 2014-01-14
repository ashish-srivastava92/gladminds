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
    # Examples:
    # url(r'^$', 'gladminds.views.home', name='home'),
    # url(r'^gladminds/', include('gladminds.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^sms/','superadmin.views.send_sms', name='send_sms'),
    url(r'^', include(admin.site.urls)),
)
