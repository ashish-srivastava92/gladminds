'''Handlers for free service coupon logic'''

import logging
from gladminds.core.services.services import Services

LOG = logging.getLogger('gladminds')

class CoreFSCService(Services):
    '''Handlers for free service coupon logic'''
    super(Services)

    def register_customer(self,sms_dict, phone_number):
        '''Register the user'''
        pass

    def send_customer_detail(self,sms_dict, phone_number):
        '''Send details of the customer'''
        pass

    def customer_service_detail(self,sms_dict, phone_number):
        '''Send details of coupons of a user'''
        pass

    def get_customer_phone_number_from_vin(self,vin):
        '''Fetches customer detail of a product'''
        pass

    def update_higher_range_coupon(self,kms, product):
        '''
        Update those coupon have higher value than the least in progress
        coupon. These case existed because some time user add higher value
        of kilometer.
        '''
        pass

    def update_exceed_limit_coupon(self,actual_kms, product):
        '''
        Exceed Limit those coupon whose kms limit is small then actual kms limit
        '''
        pass

    def get_product(self,customer_id):
        '''Fetches a product'''
        pass

    def update_coupon(self,valid_coupon, actual_kms, service_advisor, status,\
                                             update_time):
        '''Update the coupon that is valid'''
        pass

    def update_inprogress_coupon(self,coupon, actual_kms, service_advisor):
        '''Update the coupon that is in-progress'''
        pass

    def get_requested_coupon_status(self,product, service_type):
        '''Fetches the status of service type requested'''
        pass

    def validate_coupon(self,sms_dict, phone_number):
        '''Updates coupon that is valid for service'''
        pass

    def close_coupon(self,sms_dict, phone_number):
        '''Updates closing of coupon'''
        pass

    def validate_service_advisor(self,phone_number):
        '''Validates if service advisor is active'''
        pass

    def is_sa_initiator(self,coupon_id, service_advisor, phone_number):
        '''Validates if service advisor has initiated the coupon'''
        pass

    def is_valid_data(self,customer_id=None, coupon=None, sa_phone=None):
        '''Checks if customer-id and coupon number are valid'''
        pass

    def get_brand_data(self,sms_dict, phone_number):
        '''fetches brand data'''
        pass
    