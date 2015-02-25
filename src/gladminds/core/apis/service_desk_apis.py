from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie import fields
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization
from tastypie.authentication import MultiAuthentication, Authentication
from gladminds.core.model_fetcher import models
from gladminds.core.apis.user_apis import UserProfileResource

class BrandDepartmentResource(CustomBaseModelResource):
    class Meta:
        queryset = models.BrandDepartment.objects.all()
        resource_name = "brand-departments"
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True
        
class DepartmentSubCategoriesResource(CustomBaseModelResource):
    department = fields.ForeignKey(BrandDepartmentResource, 'department', null=True,
                                       blank=True, full=True)
    class Meta:
        queryset = models.DepartmentSubCategories.objects.all()
        resource_name = "department-sub-categories"
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = { 
                     "department": ALL_WITH_RELATIONS
                     } 
    

class ServiceDeskUserResource(CustomBaseModelResource):
    '''
    Service Desk User Resource
    '''
    user = fields.ForeignKey(UserProfileResource, 'user_profile',
                                        full=True, null=True, blank=True)
    sub_department = fields.ForeignKey(DepartmentSubCategoriesResource, 'sub_department', null=True,
                                       blank=True, full=True)
    
    class Meta:
        queryset = models.ServiceDeskUser.objects.all()
        resource_name = "service-desk-users"
#         authorization = MultiAuthorization(DjangoAuthorization())
#         authentication = MultiAuthentication(AccessTokenAuthentication())
        authorization = Authorization()
#         authentication = Authentication()
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                        "user": ALL_WITH_RELATIONS,
                        "sub_department": ALL_WITH_RELATIONS,
                        "sub_department__department": ALL_WITH_RELATIONS
                     }


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

    class Meta:
        queryset = models.Feedback.objects.all()
        resource_name = "feedbacks"
        authorization = MultiAuthorization(DjangoAuthorization())
        authentication = MultiAuthentication(AccessTokenAuthentication())
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                        "status": ALL,
                        "summary": ALL,
                        "created_date": ['gte', 'lte'],
                        "closed_date": ['gte', 'lte'],
                        "resolved_date": ['gte', 'lte']
                     }
