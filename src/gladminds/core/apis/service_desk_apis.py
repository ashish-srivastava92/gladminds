import datetime
from importlib import import_module
import json
import logging

from django.conf import settings
from django.conf.urls import url
from django.db import connections
from django.http.response import HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound
from tastypie import fields
from tastypie.authentication import MultiAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.utils.urls import trailing_slash

from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization, \
    ServiceDeskCustomAuthorization
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.user_apis import ServiceDeskUserResource, \
    DepartmentSubCategoriesResource, UserResource
from gladminds.core.core_utils.utils import dictfetchall
from gladminds.core.model_fetcher import models
from gladminds.core.services.service_desk.servicedesk_manager import SDActions, \
    update_feedback_activities, get_feedback
from tastypie.utils.mime import build_content_type
from gladminds.core.constants import FEEDBACK_STATUS, DEMO_PRIORITY, PRIORITIES
from gladminds.core.utils import get_list_from_set
from django.forms.models import model_to_dict


LOG = logging.getLogger('gladminds')
    
class FeedbackResource(CustomBaseModelResource):
    '''
    Service Desk Feedback Resource
    '''
    reporter = fields.ForeignKey(ServiceDeskUserResource, 'reporter', full=True,
                                 null=True, blank=True)
    assignee = fields.ForeignKey(ServiceDeskUserResource, 'assignee', full=True,
                                 null=True, blank=True)
    previous_assignee = fields.ForeignKey(ServiceDeskUserResource, 'previous_assignee',
                                          full=True, null=True, blank=True)
    sub_department = fields.ForeignKey(DepartmentSubCategoriesResource, 'sub_department',
                                       null=True, blank=True, full=True)
    

    class Meta:
        queryset = models.Feedback.objects.all()
        resource_name = "feedbacks"
        model_name = "Feedback"
        authorization = MultiAuthorization(DjangoAuthorization(), ServiceDeskCustomAuthorization())
        authentication = MultiAuthentication(AccessTokenAuthentication())
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                        "priority" : ALL,
                        "status": ALL,
                        "summary": ALL,
                        "created_date": ['gte', 'lte'],
                        "closed_date": ['gte', 'lte'],
                        "resolved_date": ['gte', 'lte'],
                        "due_date" : ['gte', 'lte'],
                        "assignee" : ALL_WITH_RELATIONS,
                        "reporter" : ALL_WITH_RELATIONS,
                        "due_date" : ALL,
                        "sub_department" : ALL_WITH_RELATIONS
                     }
        
        ordering = ['created_date','due_date']
        
    def prepend_urls(self):
        return [
                 url(r"^(?P<resource_name>%s)/add-ticket%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('add_service_desk_ticket'), name="add_service_desk_ticket"),
                url(r"^(?P<resource_name>%s)/service-desk-reports%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('get_tat'), name="get_tat"),
                url(r"^(?P<resource_name>%s)/(?P<feedback_id>\d+)/modify-ticket%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('modify_service_desk_ticket'), name="modify_service_desk_ticket"),
                url(r"^(?P<resource_name>%s)/load-analysis/(?P<args>[a-zA-Z.-]+)%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('get_load_analysis'), name="get_load_analysis")
                ]
  
    def dehydrate(self, bundle):
        if PRIORITIES.has_key(settings.BRAND):
            priority =  PRIORITIES[settings.BRAND]
        else:
            priority =  PRIORITIES['bajaj']
            
        bundle.data['STATUS'] = get_list_from_set(FEEDBACK_STATUS)
        bundle.data['PRIORITY'] = get_list_from_set(priority)
        comments = models.Comment.objects.filter(feedback_object=bundle.data['id'])
        bundle.data['comments'] = [model_to_dict(c) for c in comments]
        return bundle

    def add_service_desk_ticket(self, request, **kwargs):
        try:
            brand = settings.BRAND
            try:
                service_desk_view= getattr(import_module('gladminds.{0}.services.service_desk.servicedesk_views'.format(brand)), 'save_help_desk_data')
            except Exception as ex:
                service_desk_view= getattr(import_module('gladminds.core.services.service_desk.servicedesk_views'), 'save_help_desk_data')
            data = service_desk_view(request)
            return HttpResponse(content=json.dumps(data),
                                    content_type='application/json')
        except Exception as ex:
            LOG.error('Exception while saving data : {0}'.format(ex))
            return HttpResponseBadRequest()
    
    def get_sql_data(self, query):
        conn = connections[settings.BRAND]
        cursor = conn.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        conn.close()
        return data

    def get_tat(self, request, **kwargs):
        self.is_authenticated(request)
        details = self.get_sql_data("select sum(f2.dt) as sums ,count(*) as c , avg(f2.dt) as tat, YEAR(f1.created_date) as year, \
    MONTH(f1.created_date) as month from gm_feedback f1 inner join (select f2.id, TIMEDIFF(f2.resolved_date,f2.created_date)\
    as dt , f2.created_date from gm_feedback f2 where status= 'resolved') f2 on f2.id=f1.id group by \
    YEAR(f1.created_date), MONTH(f1.created_date)")
        reports = {}
        result = []
        for data in details:
            tat = {}
            minutes, seconds = divmod(data['tat'], 60)
            tat['tat'] = minutes
            tat['month_of_year'] = str(data['year'])+"-"+ str(data['month'])
            result.append(tat)
        reports['TAT'] = result

        fcr_total = self.get_sql_data(" select count(*) as total, concat (YEAR(resolved_date),'-', MONTH(resolved_date)) \
        as month_of_year from gm_feedback where resolved_date is not null group by \
         YEAR(resolved_date), MONTH(resolved_date)")
        
        fcr_count = self.get_sql_data("select count(*) as cnt, concat(YEAR(resolved_date), '-', MONTH(resolved_date))\
         as month_of_year from gm_feedback where fcr=1 group by(fcr),YEAR(resolved_date), MONTH(resolved_date)")
        
        result = []
        for data in fcr_total:
            fcr = {}
            fcr['month_of_year'] = data['month_of_year']
            fcrs = filter(lambda fc: fc['month_of_year'] == data['month_of_year'], fcr_count)
            if fcrs:
                fcr['fcr'] = (fcrs[0]['cnt']/float(data['total'])) * 100
            
            result.append(fcr)

        reports['FCR'] = result

        
        reopen_count = self.get_sql_data("select count(*) as cnt, concat(YEAR(created_date), '-', MONTH(created_date))\
         as month_of_year from gm_activity where new_value='Open' and original_value ='Resolved' or \
          original_value='Closed' group by YEAR(created_date), MONTH(created_date)")
         
        reopen_total = self.get_sql_data("select count(*) as total, concat(YEAR(created_date), '-', \
        MONTH(created_date)) as month_of_year from gm_feedback group by YEAR(created_date), MONTH(created_date)")
        
        result = []
        for data in reopen_total:
            reopened = {}
            reopened['month_of_year'] = data['month_of_year']
            reopens = filter(lambda reopen : reopen['month_of_year'] == data['month_of_year'], reopen_count)
            if reopens:
                reopened['re-open'] = (reopens[0]['cnt']/float(data['total'])) * 100
            result.append(reopened)
        
        reports['RE-OPENED'] = result
        
        return HttpResponse(content=json.dumps(reports),
                                    content_type='application/json')

    def modify_service_desk_ticket(self, request, **kwargs):
        self.is_authenticated(request)
        try:
            brand = settings.BRAND
            data = request.POST
            feedback_obj = get_feedback(data['ticketId'], request.user)
            host = request.get_host()
            try:
                modify_ticket = getattr(import_module('gladminds.{0}.services.service_desk.servicedesk_manager'.format(brand), 'modify_feedback'))
            except Exception as ex:
                modify_ticket = getattr(import_module('gladminds.core.services.service_desk.servicedesk_manager'), 'modify_feedback')       
            ret_value = modify_ticket(feedback_obj, data, request.user, host)
            data = {'status' : ret_value}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception as ex:
            LOG.error('Exception while modifying data : {0}'.format(ex))
            return HttpResponseBadRequest()
    
    
    def get_load_analysis(self, request, **kwargs):
        self.is_authenticated(request)
        total_tickets = []

        if kwargs['args'] == 'hourly':
            date = datetime.datetime.now().date()
            date = str(date) + "%"
            ticket_count = self.get_sql_data("select count(*) as cnt , HOUR(created_date) as hour \
            from gm_feedback where created_date like '%s' group by HOUR(created_date)" %date)
            
            for data in ticket_count:
                ticket = {}
                ticket['hour_of_the_day'] = data['hour']
                ticket['ticket_raised'] = data['cnt']
                total_tickets.append(ticket)
        
        elif kwargs['args'] == 'agents':
            ticket_count = self.get_sql_data(" select f.id , f.assignee_id, count(*) as cnt ,au.username\
             from gm_feedback f left outer join gm_servicedeskuser s on s.id= f.assignee_id left outer\
              join gm_userprofile u on s.user_profile_id=u.user_id left outer join auth_user au on \
              u.user_id = au.id group by f.assignee_id ")
            for data in ticket_count:
                ticket = {}
                ticket['agent_name'] = data['username']
                ticket['total_tickets'] = data['cnt']
                total_tickets.append(ticket)
                
        return HttpResponse(content=json.dumps(total_tickets),
                            content_type='application/json')
    
class ActivityResource(CustomBaseModelResource):
    '''
    Service Desk Activities Resource 
    '''
    feedback = fields.ForeignKey(FeedbackResource, 'feedback', full=True,
                                 null=True, blank=True)
    user = fields.ForeignKey(UserResource, 'user', full=True,
                             null=True, blank=True)
    
    class Meta:
        queryset = models.Activity.objects.all()
        resource_name = 'feedback-activities'
        detailed_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                      "user" : ALL_WITH_RELATIONS,
                      "feedback" : ALL_WITH_RELATIONS
                     }
        ordering = ['created_date']
    
class SLAResource(CustomBaseModelResource):
    '''
    Service Desk SLA Resource
    '''    
    
    class Meta:
        queryset = models.SLA.objects.all()
        resource_name = 'slas'
        model_name = 'SLA'
        authorization = MultiAuthorization(DjangoAuthorization())
        detailed_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "priority" : ALL
                     
                     }
        
class CommentsResource(CustomBaseModelResource):
    '''
    Service Desk Comments Resource
    '''
    feedback = fields.ForeignKey(FeedbackResource, 'feedback_object', null=True,
                                 blank=True, full=True)
    
    class Meta:
        queryset = models.Comment.objects.all()
        resource_name = 'comments'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "feedback" : ALL_WITH_RELATIONS,
                     "id" : ALL
                     }
        
    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/modify-comments/(?P<comment_id>\d+)%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('modify_comment'), name="modify_comment")
                ]
        
    
    def modify_comment(self, request, **kwargs):
        data = request.POST
        try:
            comment = models.Comment.objects.get(id=data['commentId'])
            previous_comment = comment.comment
            comment.comment = data['commentDescription']
            comment.modified_date = datetime.datetime.now()
            comment.save()
            update_feedback_activities(comment.feedback_object, SDActions.COMMENT_UPDATE, previous_comment,
                                       data['commentDescription'], request.user)
            return HttpResponse("Success")
    
        except Exception as ex:
            LOG.info("[Exception while modifying comment]: {0}".format(ex))
            return HttpResponseNotFound()

    
    
