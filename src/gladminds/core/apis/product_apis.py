from tastypie.constants import ALL
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie import fields 
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import models
from gladminds.core.apis.authorization import MultiAuthorization
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.user_apis import DealerResource


class ProductTypeResource(CustomBaseModelResource):
    class Meta:
        queryset = models.ProductType.objects.all()
        resource_name = "product-types"
#         authentication = AccessTokenAuthentication()
#         authorization = MultiAuthorization(DjangoAuthorization())
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True


class ProductResource(CustomBaseModelResource):
    product_type = fields.ForeignKey(ProductTypeResource, 'product_type',
                                     null=True, blank=True, full=True)
    dealer_id = fields.ForeignKey(DealerResource, 'dealer_id',
                                  null=True, blank=True, full=True)

    class Meta:
        queryset = models.ProductData.objects.all()
        resource_name = "products"
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
                     "product_id":  ALL,
                     "customer_id": ALL,
                     "customer_phone_number": ALL,
                     "customer_name": ALL,
                     "customer_address": ALL,
                     "purchase_date": ['gte', 'lte'],
                     "invoice_date": ['gte', 'lte']
                     }


class CustomerTempRegistrationResource(CustomBaseModelResource):
    product_data = fields.ForeignKey(ProductResource, 'product_data', null=True, blank=True, full=True)

    class Meta:
        queryset = models.CustomerTempRegistration.objects.all()
        resource_name = "customer-changes"
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get']
        always_return_data = True
