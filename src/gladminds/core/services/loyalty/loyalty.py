'''Handlers for loyalty service logic'''

import logging
from gladminds.core.services.services import Services

LOG = logging.getLogger('gladminds')

class CoreLoyaltyService(Services):

    def __init__(self):
        Services.__init__(self)

    def send_welcome_sms(self, mech):
        '''Send welcome message to the user'''
        pass

    def send_welcome_message(self, request):
        '''Send welcome message to the user'''
        pass

    def update_points(self, mechanic, accumulate=0, redeem=0):
        '''Update the loyalty points of the user'''
        pass
    
    def check_point_balance(self, sms_dict, phone_number):
        '''send balance point of the user'''
        pass

    def fetch_catalogue_products(self, product_codes):
        '''Fetches all the products with given upc'''
        pass

    def accumulate_point(self, sms_dict, phone_number):
        '''accumulate points with given upc'''
        pass
    
    def redeem_point(self, sms_dict, phone_number):
        '''redeem points with given upc'''
        pass

        