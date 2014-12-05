from django.conf.urls import patterns, url, include
from gladminds.afterbuy.admin import brand_admin
from tastypie.api import Api
from gladminds.afterbuy.apis import product_apis, brand_apis
from gladminds.core.apis import preferences_apis
from gladminds.afterbuy.apis import user_apis
from gladminds.core.apis.image_apis import upload_files

from provider.oauth2 import views
from provider.oauth2 import urls

api_v1 = Api(api_name="afterbuy/v1")
api_v1.register(user_apis.ConsumerResource())
api_v1.register(user_apis.InterestResource())
api_v1.register(user_apis.UserNotificationResource())
api_v1.register(user_apis.ServiceTypeResource())
api_v1.register(user_apis.ServiceResource())
api_v1.register(product_apis.ProductInsuranceInfoResource())
api_v1.register(product_apis.InvoiceResource())
api_v1.register(product_apis.LicenseResource())
api_v1.register(product_apis.UserProductResource())
api_v1.register(product_apis.RegistrationCertificateResource())
api_v1.register(product_apis.PollutionCertificateResource())
api_v1.register(product_apis.SupportResource())
api_v1.register(product_apis.ProductSupportResource())
api_v1.register(product_apis.ProductTypeResource())
api_v1.register(product_apis.SellInformationResource())
api_v1.register(product_apis.UserProductImagesResource())
api_v1.register(brand_apis.BrandResource())
api_v1.register(brand_apis.IndustryResource())
api_v1.register(brand_apis.BrandProductCategoryResource())
api_v1.register(preferences_apis.UserPreferenceResource())
api_v1.register(preferences_apis.BrandPreferenceResource())



urlpatterns = patterns('',
    url(r'', include(api_v1.urls)),
    url(r'api/doc/', include('gladminds.core.api_docs.swagger_urls', namespace='tastypie_swagger')),
    url(r'^', include(brand_admin.urls)),
    url(r'^afterbuy/v1/upload', upload_files),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^site-info/$', 'gladminds.afterbuy.views.site_info', name='site_info')
)
