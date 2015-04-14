import json

from django.conf.urls import url
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.aggregates import Count
from django.http.response import HttpResponse
from tastypie import fields 
from tastypie.authentication import MultiAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.utils.urls import trailing_slash

from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization, \
    CTSCustomAuthorization
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.user_apis import DealerResource, PartnerResource
from gladminds.core.auth_helper import Roles
from gladminds.core.model_fetcher import models


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
        authorization = MultiAuthorization(Authorization())
        detail_allowed_methods = ['get']
        filtering = {
                     "product_id":  ALL,
                     "customer_id": ALL,
                     "customer_phone_number": ALL,
                     "customer_name": ALL,
                     "customer_address": ALL,
                     "purchase_date": ['gte', 'lte', 'isnull'],
                     "invoice_date": ['gte', 'lte'],
                     "dealer_id": ALL_WITH_RELATIONS
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
        filtering = {
                      "product_data" : ALL_WITH_RELATIONS 
                     }

class ProductCatalogResource(CustomBaseModelResource):
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True, blank=True, full=True)
    
    class Meta:
        queryset = models.ProductCatalog.objects.all()
        resource_name = "product-catalogs"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class SpareMasterResource(CustomBaseModelResource):
    product_type = fields.ForeignKey(ProductTypeResource, 'product_type', full=True)
    class Meta:
        queryset = models.SparePartMasterData.objects.all()
        resource_name = "spare-masters"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class SparePartPointResource(CustomBaseModelResource):
    part_number = fields.ForeignKey(SpareMasterResource, 'part_number', full=True)
    class Meta:
        queryset = models.SparePartPoint.objects.all()
        resource_name = "spare-points"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class SparePartUPCResource(CustomBaseModelResource):
    part_number = fields.ForeignKey(SpareMasterResource, 'part_number', full=True)
    class Meta:
        queryset = models.SparePartUPC.objects.all()
        resource_name = "spare-upcs"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True


class TransporterResource(CustomBaseModelResource):
    class Meta:
        queryset = models.Transporter.objects.all()
        resource_name = 'transporters'
        authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get']
        always_return_data = True
        
class ContainerTrackerResource(CustomBaseModelResource):
    transporter = fields.ForeignKey(TransporterResource, 'transporter', null=True,
                                    blank=True, full=True)
    class Meta:
        queryset = models.ContainerTracker.objects.all()
        resource_name = 'container-trackers'
        authorization = MultiAuthorization(DjangoAuthorization(), CTSCustomAuthorization())
        authentication = MultiAuthentication(AccessTokenAuthentication())
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data =True
        filtering = {
                     'transporter': ALL_WITH_RELATIONS,
                     'transaction_id' : ALL,
                     'lr_date' : ['gte', 'lte'],
                     'gatein_date' : ['gte', 'lte'],
                     'status' : ALL,
                     "zib_indent_num" : ALL
                     
                     }
        ordering = ['lr_date', 'gatein_date' ,'created_date']
        
    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/count%s" % (self._meta.resource_name,trailing_slash()),
                self.wrap_view('get_status_count'), name="get_status_count")
                ]
        
    def  get_status_count(self, request, **kwargs):
        self.is_authenticated(request)
        if request.user.groups.filter(name=Roles.TRANSPORTER):
            data = models.ContainerTracker.objects.filter(transporter__user__user_id=request.user.id).values('status').annotate(total=Count('status'))
        elif request.user.groups.filter(name=Roles.SUPERVISOR):
            transporter = models.Supervisor.objects.get(user__user_id=request.user.id).transporter
            data = models.ContainerTracker.objects.filter(transporter=transporter).values('status').annotate(total=Count('status'))
        else:
            data = models.ContainerTracker.objects.all().values('status').annotate(total=Count('status'))
            
        return HttpResponse(content=json.dumps(list(data), cls=DjangoJSONEncoder), content_type='application/json')
