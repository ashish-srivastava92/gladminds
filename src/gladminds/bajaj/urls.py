from django.conf.urls import patterns, url, include
from django.conf import settings
from gladminds.bajaj.admin import brand_admin
from gladminds.afterbuy.apis import api_resource
from tastypie.api import Api
from gladminds.core import urls as core_urls

api_v1 = Api(api_name="v1")
# api_v1.register(audit_api.AuditResources())
# api_v1.register(user_apis.GladMindUserResources())

urlpatterns = patterns('',
   
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'', include(brand_admin.urls)),
    url(r'', include(core_urls)),
    url(r'', include(api_v1.urls))
)