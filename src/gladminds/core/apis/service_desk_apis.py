from django.conf.urls import url
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.utils.urls import trailing_slash
from tastypie.authentication import MultiAuthentication
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization
from gladminds.core.model_fetcher import models
from gladminds.core.apis.user_apis import ServiceDeskUserResource,\
    DepartmentSubCategoriesResource
    
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
    sub_department = fields.ForeignKey(DepartmentSubCategoriesResource, 'sub_department', null=True, blank=True, full=True)
        
    class Meta:
        queryset = models.Feedback.objects.all()
        resource_name = "feedbacks"
        model_name = "Feedback"
        authorization = MultiAuthorization(DjangoAuthorization())
#         authentication = MultiAuthentication(AccessTokenAuthentication())
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
                        "sub_department__department" : ALL_WITH_RELATIONS,
                        "sub_department" : ALL_WITH_RELATIONS
                     }
    
