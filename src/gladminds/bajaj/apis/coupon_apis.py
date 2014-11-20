from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import Authorization
from tastypie import fields
from gladminds.bajaj.apis.product_apis import ProductDataResources
from gladminds.bajaj.models import CouponData, ServiceAdvisor, Dealer
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.bajaj.apis.user_apis import ServiceAdvisorResources,\
    DealerResources
  
class CouponDataResources(CustomBaseModelResource):
    product = fields.ForeignKey(ProductDataResources, 'product', full=True)
    service_advisor = fields.ForeignKey(ServiceAdvisorResources, 'service_advisor', full=True, null=True, blank=True)

    class Meta:
        queryset = CouponData.objects.all()
        resource_name = "coupons"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True
        filtering = {
                        "service_type" : ALL,
                        "status" : ALL,
                        "closed_date" : ['gte', 'lte'],
                        "product" : ALL_WITH_RELATIONS,
                        "unique_service_coupon" : ALL
                     }

