from django.conf.urls import patterns, url, include
from gladminds.demo.admin import brand_admin
from gladminds.core import urls as core_urls
from django.contrib import admin
from tastypie.api import Api
from gladminds.core.apis import service_desk_apis

api_v1 = Api(api_name="v1")
api_v1.register(service_desk_apis.ServiceDeskUserResource())
api_v1.register(service_desk_apis.DepartmentSubCategoriesResource())
api_v1.register(service_desk_apis.BrandDepartmentResource())

urlpatterns = patterns('',
    url(r'^site-info/$', 'gladminds.demo.views.site_info', name='site_info'),
    url(r'^admin/', include(brand_admin.urls)),
    url(r'', include(core_urls)),
    url(r'', include(api_v1.urls))
    
)