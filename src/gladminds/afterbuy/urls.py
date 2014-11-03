from django.conf.urls import patterns, url, include
from gladminds.afterbuy.admin import brand_admin
from tastypie.api import Api
from gladminds.afterbuy.apis import product_apis
from gladminds.afterbuy.apis import user_apis

api_v1 = Api(api_name="afterbuy/v1")
api_v1.register(product_apis.ProductInsuranceInfoResource())
api_v1.register(product_apis.InvoiceResource())
api_v1.register(product_apis.LicenseResource())
api_v1.register(product_apis.UserProductResource())
api_v1.register(product_apis.RegistrationCertificateResource())
api_v1.register(product_apis.PollutionCertificateResource())
api_v1.register(user_apis.UserResources())


urlpatterns = patterns('',
    (r'', include(api_v1.urls)),
    url(r'^', include(brand_admin.urls))
)
