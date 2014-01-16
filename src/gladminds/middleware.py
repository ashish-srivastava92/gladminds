from django.conf import settings
from gladminds.models import common
from django.http import HttpResponseBadRequest
from gladminds import utils
import logging
logger = logging.getLogger(__name__)

__all__ = ['GladmindsMiddleware']

"""
Gladminds middleware to identify the user type (i.e Customer, Service Advisor and Admin). 
And set the it into request object
"""
class GladmindsMiddleware(object):
    
    def __init__(self, *args, **kwargs):
        pass
    
    #If the request is come on message APIs, then it comming from SA or 
    #Customer. Verify the customer and Dealer as per phone number and message text
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated():
            return

        if request.path is '/v1/messages':
            auth_rule = None
            message = request.body
            phone_number = None
            keyword= utils.parse_message(message)
            handler = settings.HANDLER_MAPPER.get(keyword, None)
            if handler:
                auth_rule = handler['auth_rule']
            
            if 'open' in auth_rule:
                return
            elif 'sa' in auth_rule:
                try:
                    common.ServiceAdvisor.objects.get(phone_number=phone_number)
                except common.ServiceAdvisor.DoesNotExist:
                    raise HttpResponseBadRequest() 
                
            elif 'customer' in auth_rule:
                try:
                    object = common.GladMindUsers.objects.get(phone_number=phone_number)
                except common.GladMindUsers.DoesNotExist:
                    raise HttpResponseBadRequest()
                    

        
        
        
