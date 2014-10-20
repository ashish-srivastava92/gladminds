from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import Authorization
from tastypie import fields 
from gladminds.apis.baseresource import CustomBaseResource
from gladminds.apis.user_apis import GladMindUserResources
from gladminds.bajaj.models import ProductTypeData, ProductData
   
class ProductTypeDataResources(CustomBaseResource):
    class Meta:
        queryset = ProductTypeData.objects.all()
        resource_name = "producttypes"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
   
class ProductDataResources(CustomBaseResource):
    product_type = fields.ForeignKey(ProductTypeDataResources, 'product_type', null=True, blank=True, full=True)
    customer_phone_number = fields.ForeignKey(GladMindUserResources, 'customer_phone_number',  null=True, blank=True, full=True)
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

