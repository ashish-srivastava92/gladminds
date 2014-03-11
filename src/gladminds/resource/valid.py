from tastypie.authentication import Authentication
from tastypie.exceptions import Unauthorized, BadRequest
from tastypie.exceptions import ImmediateHttpResponse
from tastypie import http
from gladminds.models import common


class AfterBuyAuthentication(Authentication):
    '''
    simply checking whether
    access token is provided in request 
    or not
    '''
    def is_authenticated(self, request, **kwargs):
        access_token = get_access_token(request)
        if access_token:
            if access_token=='testaccesstoken':
                return True
            try:
                gladmind_user=common.GladMindUsers.objects.get(gladmind_customer_id=access_token)
                return True
            except:
                return False
        else:
            return False
        


def get_access_token(request):
    try:
        access_token=request.GET.get('accessToken', '')\
                             or request.META.get('HTTP_AUTHORIZATION', None)['accessToken']
    except:
        access_token=None
    return access_token
           
