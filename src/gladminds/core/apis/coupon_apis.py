from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.authentication import GladmindsServiceAuthentication,\
    AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization,\
    CustomAuthorization
from tastypie.authentication import MultiAuthentication
from gladminds.core.auth.service_handler import Services
from gladminds.core.model_fetcher import models
from gladminds.core.apis.user_apis import ServiceAdvisorResources
from gladminds.core.apis.product_apis import ProductResource


class CouponDataResources(CustomBaseModelResource):
    product = fields.ForeignKey(ProductResource, 'product', full=True)
    service_advisor = fields.ForeignKey(ServiceAdvisorResources, 'service_advisor',
                                        full=True, null=True, blank=True)

    class Meta:
        queryset = models.CouponData.objects.all()
        resource_name = "coupons"
        authorization = MultiAuthorization(DjangoAuthorization(), CustomAuthorization())
        authentication = MultiAuthentication(GladmindsServiceAuthentication(Services.FREE_SERVICE_COUPON),
                                             AccessTokenAuthentication())
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True
        filtering = {
                        "service_type": ALL,
                        "status": ALL,
                        "closed_date": ['gte', 'lte'],
                        "product": ALL_WITH_RELATIONS,
                        "unique_service_coupon": ALL
                     }
