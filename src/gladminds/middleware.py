from django.conf import settings
from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common
from django.http import HttpResponseBadRequest
from gladminds import utils
from gladminds import smsparser
import logging
logger = logging.getLogger(__name__)

__all__ = ['GladmindsMiddleware', 'GladmindsMessageMiddleware']
SMS_CLIENT = settings.__dict__['_wrapped'].__class__.SMS_CLIENT =  utils.make_tls_property()

"""
Gladminds middleware to identify the IP from where the message request came
and reply through the same platform
"""

class GladmindsMessageMiddleware(object):    
    #If the request is come on message APIs, then based on the IP we set sms client
    def process_request(self, request, **kwargs):
        request_ip = request.META['REMOTE_ADDR']
        logger.info('[GladmindsMiddleWare]:: The request is coming from the ip {0}'.format(request_ip))
        if request_ip == '54.84.243.77':
            SMS_CLIENT.value = 'AIRTEL'
        else:
            SMS_CLIENT.value = 'KAP'

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
            message = None
            phone_number = None
            if request.POST.get('text'):
                message = request.POST.get('text')
                phone_number = request.POST.get('phoneNumber')
            else:
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
                    aftersell_common.ServiceAdvisor.objects.get(phone_number=phone_number)
                    request.user['role'] = 'SA'
                    request.user['phone_number'] = phone_number
                except aftersell_common.ServiceAdvisor.DoesNotExist:
                    raise HttpResponseBadRequest() 
                
            elif 'customer' in auth_rule:
                try:
                    object = common.GladMindUsers.objects.get(phone_number=phone_number)
                    request.user['role'] = 'Customer'
                    request.user['phone_number'] = phone_number
                except common.GladMindUsers.DoesNotExist:
                    raise HttpResponseBadRequest()
        return