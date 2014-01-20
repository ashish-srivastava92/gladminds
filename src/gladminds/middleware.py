from django.conf import settings
from gladminds.models import common
from django.http import HttpResponseBadRequest
from gladminds import utils
from gladminds import smsparser
import logging
logger = logging.getLogger(__name__)

__all__ = ['GladmindsMiddleware']

"""
Gladminds middleware to identify the user type (i.e Customer, Service Advisor and Admin). 
And set the it into request object
"""
class GladmindsMiddleware(object):    
    #If the request is come on message APIs, then it coming from SA or 
    #Customer. Verify the customer and Dealer as per phone number and message text
    def process_view(self, request, view_func, view_args, view_kwargs):
        #If user is authenticated then it's an admin user
        if request.user.is_authenticated():
            return
         
        if request.path is '/v1/messages':
            #Putting a random phone, will change once we get correct format of message
            phone_number = '+91 7834671232'
            message = request.body
            message_args= smsparser.sms_parser(message = message)
            auth_rule = message_args['auth_rule']
            
            if 'open' in auth_rule:
                request.user['role'] = 'Customer'
                request.user['phone_number'] = phone_number
                return
            
            elif 'sa' in auth_rule:
                try:
                    common.ServiceAdvisor.objects.get(phone_number=phone_number)
                    request.user['role'] = 'SA'
                    request.user['phone_number'] = phone_number
                except common.ServiceAdvisor.DoesNotExist:
                    raise HttpResponseBadRequest() 
                
            elif 'customer' in auth_rule:
                try:
                    object = common.GladMindUsers.objects.get(phone_number=phone_number)
                    request.user['role'] = 'Customer'
                    request.user['phone_number'] = phone_number
                except common.GladMindUsers.DoesNotExist:
                    raise HttpResponseBadRequest()
        return