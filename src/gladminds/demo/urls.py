from django.conf.urls import patterns, url, include
from gladminds.demo.admin import brand_admin


urlpatterns = patterns('',
    url(r'^site-info/$', 'gladminds.demo.views.site_info', name='site_info'),
    url(r'^', include(brand_admin.urls)),
)