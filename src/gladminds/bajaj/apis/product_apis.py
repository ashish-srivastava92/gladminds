from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import Authorization
from tastypie import fields 
from gladminds.bajaj.models import ProductData, ProductType
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.bajaj.apis.user_apis import DealerResources, SAProfileResource
   
class ProductTypeDataResources(CustomBaseModelResource):
    class Meta:
        queryset = ProductType.objects.all()
        resource_name = "producttypes"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
   
class ProductDataResources(CustomBaseModelResource):
    product_type = fields.ForeignKey(ProductTypeDataResources, 'product_type', null=True, blank=True, full=True)
    customer_phone_number = fields.ForeignKey(SAProfileResource, 'customer_phone_number', null=True, blank=True, full=True)
    dealer_id = fields.ForeignKey(DealerResources, 'dealer_id', null=True, blank=True, full=True)
    class Meta:
        queryset = ProductData.objects.all()
        resource_name = "products"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
                     "vin":  ALL_WITH_RELATIONS,
                     "sap_customer_id" : ALL_WITH_RELATIONS,
                     "created_on" :['gte', 'lte'],
                     "product_purchase_date" : ['gte', 'lte'],
                     "invoice_date" : ['gte', 'lte']
                     }

