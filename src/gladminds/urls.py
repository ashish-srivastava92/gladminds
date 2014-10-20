from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api
from gladminds.afterbuy.apis import api_resource
#from gladminds.apis import audit_api, preferences_apis, user_apis

from gladminds.health_check import health_check_view 

# Uncomment the next two lines to enable the admin:
from gladminds.admin import admin
#from gladminds.gm.resource.user_resource import GladmindsUserResource
# admin.autodiscover()

api_v1 = Api(api_name="v1")
#api_v1.register(resources.GladmindsResources())
#api_v1.register(resources.UserResources())
api_v1.register(api_resource.AfterBuyResources())
# api_v1.register(audit_api.AuditResources())
# api_v1.register(user_apis.GladMindUserResources())

#api_v1.register(product_apis.ProductDataResources())
#api_v1.register(coupon_apis.CouponDataResources())
#api_v1.register(preferences_apis.UserPreferencesResource())
#api_v1.register(preferences_apis.AppPreferencesResource())
# api_v1.register(resources.GladmindsResources())
# api_v1.register(resources.UserResources())
# api_v1.register(api_resource.AfterBuyResources())
# api_v1.register(audit_api.AuditResources())
# api_v1.register(product_apis.ProductDataResources())
# api_v1.register(coupon_apis.CouponDataResources())


urlpatterns = patterns('',
 #   url(r'^site-info/$', 'gladminds.views.site_info', name='site_info'),
  #  url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    #Afterbuy accesstoken URL.
   # url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
)

urlpatterns += patterns('gladminds',
    (r'', include(api_v1.urls)),
    
   # url(r'^afterbuy/otp/generate/', 'afterbuy.views.generate_otp'),
   # url(r'^afterbuy/otp/validate/', 'afterbuy.views.validate_otp'),
    #url(r'^app/logout', 'afterbuy.views.app_logout', name='app_logout'),
#     url(r'^app', 'afterbuy.views.home', name='home'),
    
    
    # After buy API
#     url(r'^v1/api/users/auth', 'afterbuy.views.get_access_token'),
# 
#     url(r'^tasks-view', 'views.sqs_tasks_view'),
#     url(r'^trigger-tasks', 'views.trigger_sqs_tasks'),
#     url(r'^tasks/', SqsHandler.as_view(task_map=_tasks_map)),
#     url(r'^health-check', 'health_check.health_check_view'),
#     url(r'^afterbuy/$', 'afterbuy.views.main', name='main'),
# 
#     url(r'^sms/','superadmin.views.send_sms', name='send_sms'),
    url(r'^', include(admin.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
