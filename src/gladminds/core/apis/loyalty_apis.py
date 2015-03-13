#from tastypie.constants import ALL
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import models
from tastypie.authorization import Authorization
from tastypie import fields
from django.db.models import Count
from gladminds.core import utils
from gladminds.core.apis.dashboard_apis import SMSReportResource 
from gladminds.core.apis.product_apis import ProductTypeResource
from django.conf.urls import url
from django.http.response import HttpResponse, HttpResponseBadRequest
import json
from django.forms.models import model_to_dict
from django.db.models.query_utils import Q
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.utils.urls import trailing_slash
from gladminds.core.apis.authorization import MultiAuthorization,\
    LoyaltyCustomAuthorization
import logging
from django.db import transaction
from gladminds.core.auth_helper import Roles
from django.db.models.aggregates import Count, Sum
import itertools
from gladminds.core.apis.user_apis import MemberResource, AreaSparesManagerResource, PartnerResource,UserResource,\
UserProfileResource,DistributorResource,RetailerResource
from gladminds.core.apis.product_apis import ProductCatalogResource,\
    SparePartUPCResource
from django.conf import settings
from gladminds.core.core_utils.utils import dictfetchall
from django.db import connections
logger = logging.getLogger("gladminds")

class TerritoryResource(CustomBaseModelResource):
    
    class Meta:
        queryset = models.Territory.objects.all()
        resource_name = "territories"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'put', 'delete']
        always_return_data = True

class StateResource(CustomBaseModelResource):
    territory = fields.ForeignKey(TerritoryResource, 'territory')
    
    class Meta:
        queryset = models.State.objects.all()
        resource_name = "states"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        filtering = {
                     "state_name":ALL, 
                     }
        
class CityResource(CustomBaseModelResource):    
    state = fields.ForeignKey(StateResource, 'state')
    
    class Meta:
        queryset = models.City.objects.all()
        resource_name = "cities"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True

class LoyaltySLAResource(CustomBaseModelResource):
    class Meta:
        queryset = models.LoyaltySLA.objects.all()
        resource_name = "slas"
        model_name = 'LoyaltySLA'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class ProductResource(CustomBaseModelResource):
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True, blank=True, full=True)
    
    class Meta:
        queryset = models.ProductCatalog.objects.all()
        resource_name = "product-catalogs"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
    
class MemberResource(CustomBaseModelResource):
    distributor = fields.ForeignKey(DistributorResource, 'registered_by_distributor', null=True, blank=True, full=True) 
    preferred_retailer = fields.ForeignKey(RetailerResource, 'preferred_retailer', null=True, blank=True, full=True)
    state = fields.ForeignKey(StateResource, 'state')
    
    class Meta:
        queryset = models.Mechanic.objects.all()
        resource_name = "members"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "state":ALL_WITH_RELATIONS,
                     "locality":ALL,
                     "district":ALL,
                     }
        
class RedemptionResource(CustomBaseModelResource):
    member = fields.ForeignKey(MemberResource, 'member')
    product_catalog = fields.ForeignKey(ProductCatalogResource, 'product')
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True, blank=True, full=True)    

    class Meta:
        queryset = models.RedemptionRequest.objects.all()
        resource_name = "redemption-requests"
        model_name = 'RedemptionRequest'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        args = {
                'display_field' : {
                                    Roles.AREASPARESMANAGERS:[],
                                    Roles.NATIONALSPARESMANAGERS:[],
                                    Roles.RPS:[],
                                    Roles.LPS:[]
                                   },
                'query_field' : {
                                  Roles.RPS:{
                                             'query':[Q(is_approved=True)],
                                             'user_name':'packed_by' 
                                             },
                                  Roles.LPS : {
                                                'query':[Q(status__in=['Shipped','Delivered'])],
                                                'user':'partner__user'
                                              },
                                  Roles.DEALERS:{
                                                 'user':'registered_by_distributor__user', 
                                                 'area':'member__registered_by_distributor__city'
                                                 }, 
                                  Roles.AREASPARESMANAGERS : {
                                                'user':'member__registered_by_distributor__asm__user__user',
                                                'area':'member__state__state_name'
                                               },
                                }
                }
        
        authorization = MultiAuthorization(Authorization(), LoyaltyCustomAuthorization
                                           (display_field=args['display_field'], query_field=args['query_field']))
        filtering = {
                     "member": ALL_WITH_RELATIONS,
                     "resolution_flag":ALL,
                     }
 
    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/members-details/(?P<status>[a-zA-Z.-]+)%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('pending_redemption_request'), name="pending_redemption_request"),
                url(r"^(?P<resource_name>%s)/count%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('count_redemption_request'), name="count_redemption_request"),
                url(r"^(?P<resource_name>%s)/points%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('points_redemption_request'), name="points_redemption_request"),
                ]


    ''' returns a dict having Count of redemption request within sla, above sla and total count'''
    def count_redemption_request (self, request, **kwargs):
        data = {}
        query = {}
        try:
            user_group = request.user.groups.values()[0]['name']
            if not request.user.groups.filter(name=Roles.RPS).exists():
                q_user = self._meta.args['query_field'][user_group]['user']
                query[q_user] = request.user
            else:
                q_user = self._meta.args['query_field'][user_group]['user_name']
                query[q_user] = request.user.username
                query['is_approved']= True
               
            total = models.RedemptionRequest.objects.values('status').annotate(total_count= Count('status')).filter(**query)   
            query['resolution_flag'] = False
            within_sla_count = models.RedemptionRequest.objects.values('status').annotate(within_sla_count= Count('status')).filter(**query)
            query['resolution_flag'] = True        
            overdue_count = models.RedemptionRequest.objects.values('resolution_flag').annotate(above_sla_count= Count('status')).filter(**query)        
        
            for a,b,c in itertools.izip_longest(total, within_sla_count, overdue_count):    
                if not type(b):
                    a['within_sla_count']= b['within_sla_count']            
                if not type(c):
                    a['above_sla_count']= c['above_sla_count']   
                a.setdefault('total_count', 0)
                a.setdefault('within_sla_count', 0)
                a.setdefault('above_sla_count', 0)                                     
                data[a['status']]= a
        except Exception as ex:
            logger.error('redemption request count requested by {0}:: {1}'.format(request.user, ex))
            data = {'status': 0, 'message': 'could not retrieve the count of redemption request'}
        return HttpResponse(json.dumps(data), content_type="application/json")


    def points_redemption_request (self, request, **kwargs):
        data = {}
        query = {}
        try:
            user_group = request.user.groups.values()[0]['name']
            q_user = self._meta.args['query_field'][user_group]['user']
            area = self._meta.args['query_field'][user_group]['area']
            query[q_user] = request.user
            total_points_list = models.RedemptionRequest.objects.filter(**query).values(area).annotate(Sum('points'))   
            data = total_points_list
        except Exception as ex:
            logger.error('redemption request points requested by {0}:: {1}'.format(request.user, ex))
            data = {'status': 0, 'message': 'could not retrieve the points of redemption request'}
        return HttpResponse(data, content_type="application/json")


    ''' List of mechanics with pending redemption request'''
    def pending_redemption_request(self,request, **kwargs):
        status = kwargs['status']
        redemptionrequests = models.RedemptionRequest.objects.filter(~Q(status=status)).select_related('member')
        requests  = []
        if request.method == 'GET':
            for redemptionrequest in redemptionrequests: 
                redemption_dict = model_to_dict(redemptionrequest.member,exclude=['expected_delivery_date','due_date','image_url'])
                redemption_dict['due_date'] = redemptionrequest.member.modified_date.strftime('%Y-%m-%dT%H:%M:%S')
                redemption_dict['registered_date'] = redemptionrequest.member.registered_date.strftime('%Y-%m-%dT%H:%M:%S')
                redemption_dict['date_of_birth'] = redemptionrequest.member.date_of_birth.strftime('%Y-%m-%dT%H:%M:%S')
                redemption_dict['image_url'] = str(redemptionrequest.member.image_url)
                requests.append(redemption_dict)
            return HttpResponse(json.dumps(requests), content_type="application/json")
        else: 
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)

       
class AccumulationResource(CustomBaseModelResource):
    member = fields.ForeignKey(MemberResource, 'member', full=True) 
    asm = fields.ForeignKey(AreaSparesManagerResource, 'asm', null=True, blank=True, full=True)
    upcs = fields.ManyToManyField(SparePartUPCResource, 'upcs', full=True)
    
    class Meta:
        queryset = models.AccumulationRequest.objects.all()
        resource_name = "accumulations"
        model_name = "AccumulationRequest"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post']
        always_return_data = True
        filtering = {
                     "member":ALL_WITH_RELATIONS,
                     }
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/members-details%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('accumulation_report_details'), name="redemption_report_details")
                ]
    def get_condition(self,conditions):
        all_conditions=[]
        for condition in conditions:
                all_conditions.append(str(condition))
        return all_conditions
        
        
    
    def accumulation_report_details(self,request, **kwargs):
        querry=''
        join="left join "
        condition=''
        querry_lp_rp1=''
        querry_lp_rp=''
        before_accumulation="(select A.member_id,"
        groups = utils.get_user_groups(request.user)
        if Roles.NATIONALSPARESMANAGERS in groups:
            nsm = models.NationalSparesManager.objects.filter(user__user=request.user)
            territories = nsm[0].territory.all()
            condition = self.get_condition(territories)
            querry = "and gm_territory.territory in %(condition)s "
            
            
            
        elif Roles.AREASPARESMANAGERS in groups:
            asm = models.AreaSparesManager.objects.filter(user__user=request.user)
            states = asm[0].state.all()
            condition = self.get_condition(states)
            querry = "and gm_state.state_name in %(condition)s "
            
        elif Roles.LOYALTYADMINS in groups or Roles.LOYALTYSUPERADMINS in groups:
            pass
        
        elif Roles.LPS in groups or Roles.RPS in groups :
            lp_rp = models.Partner.objects.filter(user__user=request.user)
            lp_rp_id = lp_rp[0].partner_id
            condition = lp_rp_id
            querry_lp_rp1 = "(select * from "
            join = "right join "
            querry_lp_rp = " where member_id in (select gm_redemptionrequest.member_id from gm_redemptionrequest where partner_id = (select gm_partner.id from gm_partner where gm_partner.partner_id= %(condition)s) group by (gm_redemptionrequest.member_id)))B"
            before_accumulation="(select B.member_id,"
        else:
            return HttpResponseBadRequest()
          
        members = self.get_total_accumulated_redemption_requsets(condition,querry,join,querry_lp_rp,querry_lp_rp1,before_accumulation)    
        requests  = []   
        if request.method == 'GET':
            details = {}
            for member in members: 
                member_dict = {}
                id = member['permanent_id']
                if id != None:
                    member_dict['name'] = member['first_name'] + " " + member['middle_name'] + " " + member['last_name']
                    member_dict['registration_date'] = member['registered_date'].strftime('%d-%m-%Y')
                    member_dict['location'] = member['address_line_1'] + " " + member['address_line_2'] + " " + member['address_line_3'] + " " + member['address_line_4'] + " " + member['address_line_5'] + " " + member['address_line_6']
                    member_dict['city'] = member['district']
                    member_dict['state'] = member['state']
                    member_dict['area'] = member['locality']
                    member_dict['region'] = member['territory']
                    if member['accumulation_requests']==None:
                        member_dict['accumulation_requests'] = 0
                    else:
                        member_dict['accumulation_requests'] = member['accumulation_requests']
                    if member['accumulated_points'] != None:
                        member_dict['accumulated_points'] = int(member['accumulated_points'])
                    else:
                        member_dict['accumulated_points'] = 0
                    if member['redemption_requests']==None:
                        member_dict['redemption_requests'] = 0
                    else:
                        member_dict['redemption_requests'] = member['redemption_requests']
                    if member['redeemed_points'] != None:
                        member_dict['redeemed_points'] = int(member['redeemed_points'])
                    else:
                        member_dict['redeemed_points'] = 0
                    details[id]=member_dict
            requests.append(details)       
            return HttpResponse(json.dumps(requests), content_type="application/json")
    
    def get_total_accumulated_redemption_requsets(self,condition,querry,join,querry_lp_rp,querry_lp_rp1,before_accumulation):
        member_query =  "select * from \
                         (select gm_mechanic.id,permanent_id,first_name,middle_name,last_name,address_line_1,address_line_2,address_line_3,address_line_4,address_line_5,address_line_6,registered_date,district,locality,gm_territory.territory as territory, state_name as state \
                         from gm_territory,gm_mechanic,gm_state \
                         where gm_mechanic.state_id=gm_state.id \
                         and \
                         gm_state.territory_id=gm_territory.id "                             
        middle_querry = ")C "
            
        accumlations="A.accumulation_requests,A.accumulated_points,B.redemption_requests,B.redeemed_points \
                                   from \
                                   (select gm_accumulationrequest.member_id,count(gm_accumulationrequest.member_id) as accumulation_requests,\
                                   sum(gm_accumulationrequest.points) as accumulated_points \
                                   from \
                                   gm_accumulationrequest \
                                   group by(gm_accumulationrequest.member_id))A "
        redemptions="(select gm_redemptionrequest.member_id,count(gm_redemptionrequest.member_id) as redemption_requests,\
                                   sum(gm_redemptionrequest.points) as redeemed_points from gm_redemptionrequest group by(gm_redemptionrequest.member_id))B "                                       
        querry_end=" on A.member_id = B.member_id)D on C.id=D.member_id;"            
        member_objects = self.get_sql_data(member_query + querry + middle_querry + join + before_accumulation + accumlations + join + querry_lp_rp1 + redemptions + querry_lp_rp + querry_end,filters={'condition':condition})
        return member_objects
     
    def get_sql_data(self,query, filters={}):
        conn = connections[settings.BRAND]
        cursor = conn.cursor()
        cursor.execute(query, filters)
        data = dictfetchall(cursor)
        conn.close()
        return data
            

class WelcomeKitResource(CustomBaseModelResource):
    member = fields.ForeignKey(MemberResource, 'member')
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True, blank=True, full=True)
    
    class Meta:
        queryset = models.WelcomeKit.objects.all()
        resource_name = "welcome-kits"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class CommentThreadResource(CustomBaseModelResource):
    redemption = fields.ForeignKey(RedemptionResource, 'redemption', null=True, blank=True, full=True)
    welcome_kit = fields.ForeignKey(WelcomeKitResource, 'welcome_kit', null=True, blank=True, full=True)
    user = fields.ForeignKey(UserResource, 'user')
    
    class Meta:
        queryset = models.CommentThread.objects.all()
        resource_name = "comment-threads"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class DiscrepantAccumulationResource(CustomBaseModelResource):
    upc = fields.ForeignKey(SparePartUPCResource,'upc', null=True, blank=True, full=True)
    new_member = fields.ForeignKey(MemberResource,'new_member')
    accumulation_request = fields.ForeignKey(AccumulationResource, 'accumulation_request')
     
    class Meta:
        queryset = models.DiscrepantAccumulation.objects.all()
        resource_name = "accumulation-discrepancies"
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True

    def prepend_urls(self):
        return [
              url(r"^(?P<resource_name>%s)/transfer-points%s" % (self._meta.resource_name,trailing_slash()),
                                                     self.wrap_view('transfer_points'), name="transfer_points")
                ]

    
    def transfer_points(self,request, **kwargs):
        try:
            with transaction.atomic():
                upc = request.POST['upc']
                upc_obj = models.SparePartUPC.objects.get(unique_part_code=upc)
                points = models.SparePartPoint.objects.get(part_number=upc_obj.part_number).points
                from_mechanic = models.Mechanic.objects.get(mechanic_id= request.POST['from'])
                to_mechanic = models.Mechanic.objects.get(mechanic_id= request.POST['to'])
                self.update_points(from_mechanic, redeem=points)
                self.update_points(to_mechanic, accumulate=points)
                 
                accumulation_log = models.AccumulationRequest(member=to_mechanic,points=points,
                                                              total_points=to_mechanic.total_points,is_transferred=True)            
                accumulation_log.save()
                accumulation_log.upcs.add(upc_obj)
                data = {'status':1, 'message': 'Successfully transfered'}
        except Exception as ex:
            logger.error('[transfer_point]:{0}:: {1}'.format(upc, ex))
            data = {'status': 0, 'message': 'could not transfer points'}
        return HttpResponse(json.dumps(data), content_type="application/json")   
    
    def update_points(self, mechanic, accumulate=0, redeem=0):
        '''Update the loyalty points of the user'''
        total_points = mechanic.total_points + accumulate -redeem
        mechanic.total_points = total_points
        mechanic.save()
