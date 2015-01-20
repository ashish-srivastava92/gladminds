'''Handlers for free service coupon logic'''

import logging
from gladminds.core.services.services import Services

LOG = logging.getLogger('gladminds')

class CoreServiceDeskService(Services):
    '''Handlers for free service coupon logic'''
    super(Services)

    def service_desk(self,request):
        '''Fetches all the tickets'''
        pass

    def enable_servicedesk(self,request):
        '''Enable/diable serice desk'''
        pass

    def save_help_desk_data(self,request):
        '''Save the tickets details'''
        pass

    def get_servicedesk_tickets(self,request):
        '''Get the service desk tickets'''
        pass

    def modify_servicedesk_tickets(self,request, feedback_id):
        '''modify service desk tickets'''
        pass

    def modify_feedback_comments(self,request, feedback_id, comment_id):
        '''modify feedback comments'''
        pass

    def get_feedback_response(self,request, feedback_id):
        '''get feedback response'''
        pass

