from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from tastypie.authentication import Authentication
from provider.oauth2.models import AccessToken
import logging
from gladminds.core.auth.service_handler import ServiceHandler
from gladminds.core.loaders.module_loader import get_model


class AuthError(RuntimeError):
    '''
    General exception class.
    '''
    def __init__(self, message='OAuth error occured.'):
        self.message = message


class AccessTokenAuthentication(Authentication):

    def is_authenticated(self, request, **kwargs):
        try:
            try:
                access_token_container = request.GET.urlencode().split('access_token=')[1]
                key = access_token_container.split('&')[0]
            except:
                key = request.META.get('HTTP_ACCESS_TOKEN')
            if not key:
                logging.error('AccessTokenAuthentication. No Access Token found.')
                return None
            '''
            If verify_access_token() does not pass, it will raise an error
            '''
            token_obj = self.verify_access_token(key)
            request.user = token_obj.user
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
        if  (settings.ENV in settings.IGNORE_ENV and key in settings.HARCODED_TOKEN):
            return key
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


class GladmindsServiceAuthentication(Authentication):
    def __init__(self, service):
        self.service = service

    def is_authenticated(self, request, **kwargs):
        if ServiceHandler.check_service_enabled(self.service):
            return True
        return False
