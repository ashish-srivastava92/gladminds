from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import Authorization
from tastypie import fields 
from django.contrib.auth.models import User
from gladminds.apis.baseresource import CustomBaseResource
from gladminds.gm.models import GladmindsUser
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone
from tastypie.authentication import Authentication
from provider.oauth2.models import AccessToken
import logging


class AuthError(RuntimeError):
    '''
    General exception class.
    '''
    def __init__(self, message='OAuth error occured.'):
        self.message = message


class AccessTokenAuthentication(Authentication):
    
    def is_authenticated(self, request, **kwargs):
        try:
            access_token_container = request.GET.urlencode().split('accessToken=')[1]
            key = access_token_container.split('&')[0]
            if not key:
                logging.error('AccessTokenAuthentication. No Access Token found.')
                return None
            '''
            If verify_access_token() does not pass, it will raise an error
            '''
            self.verify_access_token(key)
            return True
        except KeyError, e:
            logging.exception('Error in Authentication. {0}'.format(e))
            request.user = AnonymousUser()
            return False
        except Exception, e:
            logging.exception('Error in Authentication. {0}'.format(e))
            return False
        return True
    
    def verify_access_token(self, key):
        try:
            token = AccessToken.objects.get(token=key)
            # Check if token has expired
            if token.expires < timezone.now():
                raise AuthError('AccessToken has expired.')
        except AccessToken.DoesNotExist, e:
            logging.info('InValid access : {0}'.format(e))
            raise AuthError('AccessToken not found at all.')
    
        logging.info('Valid access')
        return token

class UserResource(CustomBaseResource):
    class Meta:
        queryset = User.objects.all()
        print "user",queryset
        resource_name = 'users'
        excludes = ['password']
        authorization= Authorization()
        detail_allowed_methods =['get', 'post', 'put', 'delete']
        always_return_data = True
         
class GladMindUserResources(CustomBaseResource):
#     user = fields.OneToOneField(User, 'user', full=True)
    class Meta:
        queryset = GladmindsUser.objects.all()
        resource_name = 'gmusers'
        authorization= Authorization()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
                     "user":  ALL_WITH_RELATIONS,
                     "phone_number" : ALL
                     }
        always_return_data = True
