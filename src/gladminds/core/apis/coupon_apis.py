from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from gladminds.bajaj.apis.product_apis import ProductDataResources
from gladminds.bajaj.models import CouponData
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.bajaj.apis.user_apis import ServiceAdvisorResources
from gladminds.core.apis.authentication import AccessTokenAuthentication,\
    GladmindsServiceAuthentication
from gladminds.core.apis.authorization import MultiAuthorization
from tastypie.authentication import MultiAuthentication
from gladminds.core.auth.service_handler import Services
from gladminds.core.loaders.module_loader import get_model


class CouponDataResources(CustomBaseModelResource):
    product = fields.ForeignKey(ProductDataResources, 'product', full=True)
    service_advisor = fields.ForeignKey(ServiceAdvisorResources, 'service_advisor',
                                        full=True, null=True, blank=True)

    class Meta:
        queryset = get_model('CouponData').objects.all()
        resource_name = "coupons"
        authorization = MultiAuthorization(Authorization())
        authentication = MultiAuthentication(GladmindsServiceAuthentication(Services.FREE_SERVICE_COUPON))
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True
        filtering = {
                        "service_type": ALL,
                        "status": ALL,
                        "closed_date": ['gte', 'lte'],
                        "product": ALL_WITH_RELATIONS,
                        "unique_service_coupon": ALL
                     }

