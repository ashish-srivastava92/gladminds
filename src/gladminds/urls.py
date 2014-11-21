from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api

from gladminds.admin import admin
from gladminds.gm.apis import brand_apis
from gladminds.core.apis import preferences_apis

api_v1 = Api(api_name="v1")
api_v1.register(brand_apis.IndustryResource())
api_v1.register(brand_apis.BrandProductCategoryResource())
api_v1.register(brand_apis.BrandResource())
api_v1.register(brand_apis.ServiceResource())
api_v1.register(brand_apis.ServiceTypeResource())
api_v1.register(preferences_apis.BrandPreferenceResource())

urlpatterns = patterns('',
)

urlpatterns += patterns('gladminds',
    url(r'', include(api_v1.urls)),
    url(r'api/doc/', include('gladminds.core.api_docs.swagger_urls', namespace='tastypie_swagger')),
    url(r'^', include(admin.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
