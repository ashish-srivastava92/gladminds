from django.conf.urls import patterns, url, include
from gladminds.demo.admin import brand_admin
from gladminds.core import urls as core_urls
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^site-info/$', 'gladminds.demo.views.site_info', name='site_info'),
    url(r'^admin/', include(brand_admin.urls)),
    url(r'', include(core_urls)),
    
)