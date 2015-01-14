from django.contrib.auth.models import AnonymousUser
from tastypie.authentication import Authentication
import logging
from gladminds.core.auth.service_handler import ServiceHandler
from gladminds.core.auth.access_token_handler import verify_access_token


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
            token_obj = verify_access_token(key)
            request.META['HTTP_ACCESS_TOKEN'] = key
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


class GladmindsServiceAuthentication(Authentication):
    def __init__(self, service):
        self.service = service

    def is_authenticated(self, request, **kwargs):
        if ServiceHandler.check_service_enabled(self.service):
            return True
        return False
