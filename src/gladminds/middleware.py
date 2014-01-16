from django.conf import settings
from gladminds.models import common
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
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated():
            print "This is an admin user, which sent this request"
        
        if request.path is '/v1/messages':
            auth_rule = None
            message = request.body
            phone_number = None
            keyword= utils.parse_message(message)
            handler = settings.HANDLER_MAPPER.get(keyword, None)
            if handler:
                auth_rule = handler['auth_rule']
            
            if 'open' in auth_rule:
                pass
            elif 'sa' in auth_rule:
                object = common.ServiceAdvisor.objects.get(phone_number=phone_number)
            elif 'customer' in auth_rule:
                object = common.GladMindUsers.objects.get(phone_number=phone_number)
            
            
             
        
        
        #If the request is come on message APIs, then it comming from SA or 
        #Customer. Verify the customer and Dealer as per phone number and message text
        
        
        
