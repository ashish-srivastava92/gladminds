from django.conf.urls import patterns, url, include
from django.conf import settings
from gladminds.bajaj.admin import brand_admin
from gladminds.bajaj.apis import resources, product_apis, coupon_apis
from gladminds.afterbuy.apis import api_resource
from tastypie.api import Api
from gladminds.core import urls as core_urls

api_v1 = Api(api_name="v1")
api_v1.register(resources.GladmindsResources())
api_v1.register(resources.UserResources())
# api_v1.register(audit_api.AuditResources())
# api_v1.register(user_apis.GladMindUserResources())
api_v1.register(product_apis.ProductDataResources())
api_v1.register(coupon_apis.CouponDataResources())

urlpatterns = patterns('',
    url(r'^', include(core_urls)),
    url(r'^site-info/$', 'gladminds.bajaj.views.site_info', name='site_info'),
    url(r'^', include(brand_admin.urls)),
    (r'', include(api_v1.urls))
)