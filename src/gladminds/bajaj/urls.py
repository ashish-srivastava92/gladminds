from django.conf.urls import patterns, url, include
from gladminds.bajaj.admin import brand_admin


urlpatterns = patterns('',
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'^', include(brand_admin.urls)),
)