from django.conf.urls import patterns, url
from .swagger_views import SwaggerView, ResourcesView, SchemaView

urlpatterns = patterns('',
    url(r'^$', SwaggerView.as_view(), name='index'),
    url(r'^resources/$', ResourcesView.as_view(), name='resources'),
    url(r'^schema/(?P<resource>\S+)/$', SchemaView.as_view()),
    url(r'^schema/$', SchemaView.as_view(), name='schema'),
)
