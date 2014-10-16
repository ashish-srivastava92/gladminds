from django.conf.urls import patterns, url, include
from django.conf import settings
from gladminds.bajaj.admin import brand_admin
from gladminds.core import urls as core_urls


urlpatterns = patterns('',
    url(r'^', include(core_urls)),
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'^', include(brand_admin.urls)),
)