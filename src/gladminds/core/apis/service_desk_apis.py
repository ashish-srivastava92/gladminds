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
    update_feedback_activities


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
                        "assignee" : ALL_WITH_RELATIONS,
                        "due_date" : ALL,
                        "sub_department" : ALL_WITH_RELATIONS
                     }
        
        ordering = ['created_date']
        
    def prepend_urls(self):
        return [
                 url(r"^(?P<resource_name>%s)/add-ticket%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('add_service_desk_ticket'), name="add_service_desk_ticket"),
                url(r"^(?P<resource_name>%s)/tat-report%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('get_tat'), name="get_tat"),
                url(r"^(?P<resource_name>%s)/modify-ticket/(?P<feedback_id>\d+)%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('modify_service_desk_ticket'), name="modify_service_desk_ticket")
                ]
         
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
    
    def get_tat(self, request, **kwargs):
        conn = connections[settings.BRAND]
        cursor = conn.cursor()
        cursor.execute("select sum(f2.dt) as sums ,count(*) as c , avg(f2.dt) as tat, YEAR(f1.created_date) as year, \
    MONTH(f1.created_date) as month from gm_feedback f1 inner join (select f2.id, TIMEDIFF(f2.resolved_date,f2.created_date)\
    as dt , f2.created_date from gm_feedback f2 where status= 'resolved') f2 on f2.id=f1.id group by \
    YEAR(f1.created_date), MONTH(f1.created_date)")
        details = dictfetchall(cursor)
        conn.close()
        result = []
        for data in details:
            tat ={}
            minutes, seconds = divmod(data['tat'], 60)
            tat['tat'] = minutes
            tat['month_of_year'] = str(data['year'])+"-"+ str(data['month'])
            result.append(tat)
        reports = {}
        reports['TAT'] = result
        return HttpResponse(content=json.dumps(reports),
                                    content_type='application/json')

    def modify_service_desk_ticket(self, request, **kwargs):
        try:
            brand = settings.BRAND
            try:
                modify_ticket = getattr(import_module('gladminds.{0}.services.service_desk.servicedesk_views'.format(brand), 'modify_servicedesk_tickets'))
            except Exception as ex:
                modify_ticket = getattr(import_module('gladminds.core.services.service_desk.servicedesk_views'), 'modify_servicedesk_tickets')       
            return modify_ticket(request, kwargs['feedback_id'])
        except Exception as ex:
            LOG.error('Exception while modifying data : {0}'.format(ex))
            return HttpResponseBadRequest()
    
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

    
    
