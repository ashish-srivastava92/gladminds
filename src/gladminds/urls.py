from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api

from gladminds.admin import admin
from gladminds.default.apis import brand_apis
from gladminds.core.apis import preferences_apis
from gladminds.core.cron_jobs.taskqueue import SqsHandler
from gladminds.sqs_tasks import _tasks_map
from gladminds.core.views import sqs_tasks_view, trigger_sqs_tasks

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
    url(r'^tasks-view/', sqs_tasks_view),
    url(r'^trigger-tasks', trigger_sqs_tasks),
    url(r'^tasks', SqsHandler.as_view(task_map=_tasks_map)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
