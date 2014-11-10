from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api

from gladminds.admin import admin
from gladminds.gm.apis import brand_apis

api_v1 = Api(api_name="v1")
api_v1.register(brand_apis.IndustryResource())
api_v1.register(brand_apis.BrandCategoryResource())
api_v1.register(brand_apis.BrandResource())


urlpatterns = patterns('',
)

urlpatterns += patterns('gladminds',
    (r'', include(api_v1.urls)),
    url(r'^', include(admin.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
