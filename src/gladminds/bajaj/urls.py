from django.conf.urls import patterns, url, include
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'^', include(admin.site.urls)),
)