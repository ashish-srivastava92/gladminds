from django.conf.urls import patterns, url, include
from gladminds.bajaj.admin import brand_admin
from gladminds.bajaj.resource import resources, product_apis
from gladminds.afterbuy import api_resource
from gladminds.apis import user_apis
from tastypie.api import Api

api_v1 = Api(api_name="v1")
api_v1.register(resources.GladmindsResources())
api_v1.register(resources.UserResources())
# api_v1.register(audit_api.AuditResources())
# api_v1.register(user_apis.GladMindUserResources())
# api_v1.register(product_apis.ProductDataResources())

urlpatterns = patterns('',
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'^', include(brand_admin.urls)),
)