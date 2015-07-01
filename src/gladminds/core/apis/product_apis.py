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
    CTSCustomAuthorization, ContainerLRCustomAuthorization, \
    ContainerIndentCustomAuthorization
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.user_apis import DealerResource, PartnerResource,\
    TransporterResource
from gladminds.core.auth_helper import Roles
from gladminds.core.model_fetcher import get_model
from django.db.models.query_utils import Q
import operator
from datetime import date, datetime, timedelta
import logging

LOG = logging.getLogger('gladminds')

class ProductTypeResource(CustomBaseModelResource):
    class Meta:
        queryset = get_model('ProductType').objects.all()
        resource_name = "product-types"
#         authentication = AccessTokenAuthentication()
#         authorization = MultiAuthorization(DjangoAuthorization())
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True


class ProductResource(CustomBaseModelResource):
    product_type = fields.ForeignKey(ProductTypeResource, 'product_type',
                                     null=True, blank=True, full=True)
    dealer_id = fields.ForeignKey(DealerResource, 'dealer_id',
                                  null=True, blank=True, full=True)

    class Meta:
        queryset = get_model('ProductData').objects.all()
        resource_name = "products"
#         authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(Authorization())
        allowed_methods = ['get']
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
        queryset = get_model('CustomerTempRegistration').objects.all()
        resource_name = "customer-changes"
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization())
        allowed_methods = ['get']
        always_return_data = True
        filtering = {
                      "product_data" : ALL_WITH_RELATIONS 
                     }

class ProductCatalogResource(CustomBaseModelResource):
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True, blank=True, full=True)
    
    class Meta:
        queryset = get_model('ProductCatalog').objects.all()
        resource_name = "product-catalogs"
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class SpareMasterResource(CustomBaseModelResource):
    product_type = fields.ForeignKey(ProductTypeResource, 'product_type', full=True)
    class Meta:
        queryset = get_model('SparePartMasterData').objects.all()
        resource_name = "spare-masters"
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class SparePartPointResource(CustomBaseModelResource):
    part_number = fields.ForeignKey(SpareMasterResource, 'part_number', full=True)
    class Meta:
        queryset = get_model('SparePartPoint').objects.all()
        resource_name = "spare-points"
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class SparePartUPCResource(CustomBaseModelResource):
    part_number = fields.ForeignKey(SpareMasterResource, 'part_number', full=True)
    class Meta:
        queryset = get_model('SparePartUPC').objects.all()
        resource_name = "spare-upcs"
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class ContainerIndentResource(CustomBaseModelResource):

    class Meta:
        queryset = get_model('ContainerIndent').objects.all()
        resource_name = 'container-indents'
        authorization = MultiAuthorization(DjangoAuthorization(), ContainerIndentCustomAuthorization())
        authentication = MultiAuthentication(AccessTokenAuthentication())
        allowed_methods = ['get', 'put', 'post']
        always_return_data =True
        filtering = {
                     'created_date': ALL,
                     'modified_date': ALL,
                     'indent_num' : ALL,
                     'no_of_containers': ALL,
                     'status' : ALL,
                     }
        
        ordering = ['status', 'indent_num' ,'created_date', 'modified_date']

    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/count%s" % (self._meta.resource_name,trailing_slash()),
                self.wrap_view('get_status_count'), name="get_status_count")
                ]
        
    def  get_status_count(self, request, **kwargs):
        self.is_authenticated(request)
        args = request.GET
        from_date = args.get('from', datetime.now() - timedelta(days=180))
        to_date = args.get('to', datetime.now())
        query_args = [Q(created_date__range=[from_date, to_date])]
        try:
            if request.user.groups.filter(name=Roles.TRANSPORTER):
                submitted_indents = get_model('ContainerLR').objects.filter(transporter__user__user_id=request.user.id
                                                                    ).values_list('zib_indent_num_id', flat=True)
            elif request.user.groups.filter(name=Roles.SUPERVISOR):
                supervisor = get_model('Supervisor').objects.get(user__user_id=request.user.id)
                submitted_indents = get_model('ContainerLR').objects.filter(Q(submitted_by=supervisor.supervisor_id) | Q(submitted_by=None) 
                                                                        & Q(transporter=supervisor.transporter
                                                                    )).values_list('zib_indent_num_id', flat=True)
            query_args.append(Q(id__in=submitted_indents))
            data = get_model('ContainerIndent').objects.filter(reduce(operator.and_, query_args)
                                                              ).values('status').annotate(total=Count('status')).order_by('-status')
        except Exception as ex:
            LOG.error('Exception while obtaining CTS count : {0}'.format(ex))
        return HttpResponse(content=json.dumps(list(data), cls=DjangoJSONEncoder), content_type='application/json')

class ContainerLRResource(CustomBaseModelResource):
    zib_indent_num = fields.ForeignKey(ContainerIndentResource, 'zib_indent_num', null=True,
                                    blank=True, full=True)
    transporter = fields.ForeignKey(TransporterResource, 'transporter', null=True, blank=True)

    class Meta:
        queryset = get_model('ContainerLR').objects.all()
        resource_name = 'container-lrs'
        authorization = MultiAuthorization(DjangoAuthorization(), ContainerLRCustomAuthorization())
        authentication = MultiAuthentication(AccessTokenAuthentication())
        allowed_methods = ['get', 'put']
        always_return_data =True
        filtering = {
                     'zib_indent_num': ALL_WITH_RELATIONS,
                     'transaction_id' : ALL,
                     'lr_date' : ALL,
                     'gatein_date' :ALL,
                     'status' : ALL,
                     'created_date': ALL,
                     'modified_date': ALL,
                     'submitted_by': ALL,
                     'transporter': ALL_WITH_RELATIONS
                     }
        
        ordering = ['lr_date', 'gatein_date' ,'created_date', 'status']

    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/save/(?P<transaction_id>\d+)%s" % (self._meta.resource_name,trailing_slash()),
                self.wrap_view('save_lr'), name="save_lr")
                ]
        
    def  save_lr(self, request, **kwargs):
        '''Saves the status of individual LR and 
        update status of indent accordingly
        args:
         transaction_id: the primary key to identify the LR
         status: new status to be saved
        '''
        self.is_authenticated(request)
        transaction_id=kwargs['transaction_id']
        load = json.loads(request.body)
        status = load.get('status', None)
        try:
            conatiner_lr = get_model('ContainerLR').objects.get(transaction_id=transaction_id)
            conatiner_lr.status = status
            if status=='Inprogress':
                conatiner_lr.submitted_by = request.user.username
            conatiner_lr.save()
            container_indent=conatiner_lr.zib_indent_num
            if status=='Open':
                container_indent.status = status
                container_indent.save()
            else:
                all_indent_lr = get_model('ContainerLR').objects.filter(zib_indent_num=container_indent, status=status)
                if len(all_indent_lr)==container_indent.no_of_containers:
                    container_indent.status = status
                    container_indent.save()
            data=[{'message': 'LR status updated successfully'}]
        except Exception as ex:
            data=[{'message': 'LR status update unsuccessful'}]
            LOG.error('Exception while obtaining CTS count : {0}'.format(ex))
        return HttpResponse(content=json.dumps(list(data), cls=DjangoJSONEncoder), content_type='application/json')


class ContainerTrackerResource(CustomBaseModelResource):
    transporter = fields.ForeignKey(TransporterResource, 'transporter', null=True,
                                    blank=True, full=True)
    class Meta:
        queryset = get_model('ContainerTracker').objects.all()
        resource_name = 'container-trackers'
        authorization = MultiAuthorization(DjangoAuthorization(), CTSCustomAuthorization())
        authentication = MultiAuthentication(AccessTokenAuthentication())
        allowed_methods = ['get', 'post', 'put']
        always_return_data =True
        filtering = {
                     'transporter': ALL_WITH_RELATIONS,
                     'transaction_id' : ALL,
                     'lr_date' : ALL,
                     'gatein_date' :ALL,
                     'status' : ALL,
                     'zib_indent_num' : ALL,
                     'created_date': ALL,
                     'submitted_by': ALL,
                     'modified_date': ALL
                     }
        
        ordering = ['lr_date', 'gatein_date' ,'created_date', 'status']
        
    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/count%s" % (self._meta.resource_name,trailing_slash()),
                self.wrap_view('get_status_count'), name="get_status_count")
                ]
        
    def  get_status_count(self, request, **kwargs):
        self.is_authenticated(request)
        args = request.GET
        from_date = args.get('from', datetime.now() - timedelta(days=180))
        to_date = args.get('to', datetime.now())
        query_args = [Q(created_date__range=[from_date, to_date])]
        try:
            if request.user.groups.filter(name=Roles.TRANSPORTER):
                supervisor_id = args.get('supervisor_id', None)
                query_args.append(Q(transporter__user_id=request.user.id))
                if supervisor_id:
                    query_args.append(Q(submitted_by=supervisor_id))
                indent_list = get_model('ContainerTracker').objects.filter(reduce(operator.and_, query_args)
                                                              ).values_list('zib_indent_num', flat=True).distinct()
            elif request.user.groups.filter(name=Roles.SUPERVISOR):
                supervisor = get_model('Supervisor').objects.get(user__user_id=request.user.id)
                query_args.append(Q(transporter=supervisor.transporter))
                indent_list = get_model('ContainerTracker').objects.filter(reduce(operator.and_, query_args) &
                                                              (Q(submitted_by=supervisor.supervisor_id)| Q(submitted_by=None))
                                                              ).values_list('zib_indent_num', flat=True).distinct()
            else:
                indent_list = get_model('ContainerTracker').objects.filter(reduce(operator.and_, query_args)
                                                              ).values_list('zib_indent_num', flat=True).distinct()
            open_indent=get_model('ContainerTracker').objects.filter(zib_indent_num__in=indent_list, status='Open').values_list('zib_indent_num', flat=True).distinct()
            remaining_indent=list(set(indent_list).difference(open_indent))
            inporgress_indent=get_model('ContainerTracker').objects.filter(zib_indent_num__in=remaining_indent, status='Inprogress').values_list('zib_indent_num', flat=True).distinct()
            data=[{'status':'Open', 'total':len(open_indent)},{'status':'Inprogress','total':len(inporgress_indent)}]
        except Exception as ex:
            LOG.error('Exception while obtaining CTS count : {0}'.format(ex))
        return HttpResponse(content=json.dumps(list(data), cls=DjangoJSONEncoder), content_type='application/json')
