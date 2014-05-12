from unittest import TestCase
from datetime import datetime, timedelta
from gladminds.utils import get_sa_list

class TestAssertWorks(TestCase):

    def test_assert_equals(self):
        self.assertEquals(100, 100, '100 == 100')

    def test_assert_true(self):
        self.assertTrue(100 > 1, '100 > 1')

class TestUtils(TestCase):
    
    def setUp(self):
        super(TestUtils, self).setUp()
        brand_obj = self.get_brand_obj(brand_id='brand001', brand_name='bajaj')
        product_type_obj = self.get_product_type_obj(brand_id=brand_obj, product_name='DISCO120', product_type='BIKE')
        dealer_obj = self.get_delear_obj(dealer_id='DEALER001')
        customer_obj = self.get_customer_obj(phone_number='+919999999')
        product_obj = self.get_product_obj(vin="VINXXX001", product_type=product_type_obj, dealer_id=dealer_obj\
                                           , customer_phone_number=customer_obj, sap_customer_id='SAP001')
        service_advisor = self.get_service_advisor_obj(service_advisor_id='SA001Test', name='UMOTO', phone_number='+914444861111')
        self.get_dealer_service_advisor_obj(dealer_id=dealer_obj, service_advisor_id=service_advisor, status='Y')
        service_advisor1 = self.get_service_advisor_obj(service_advisor_id='SA002Test', name='UMOTOR', phone_number='+919999999999')
        self.get_dealer_service_advisor_obj(dealer_id=dealer_obj, service_advisor_id=service_advisor1, status='Y')
        self.get_coupon_obj(unique_service_coupon='COUPON005', vin=product_obj, valid_days=30, valid_kms=500\
                            , service_type=1, status=1, mark_expired_on=datetime.now() - timedelta(days=2)\
                            , actual_service_date=datetime.now() - timedelta(days=20), extended_date=datetime.now() - timedelta(days=2))
        customer_obj1 = self.get_customer_obj(phone_number='8888888')
        product_obj1 = self.get_product_obj(vin="VINXXX002", product_type=product_type_obj, dealer_id=dealer_obj\
                                           , customer_phone_number=customer_obj1, sap_customer_id='SAP002')
        self.get_coupon_obj(unique_service_coupon='COUPON004', vin=product_obj1, valid_days=30, valid_kms=500\
                            , service_type=1, status=1, mark_expired_on=datetime.now() - timedelta(days=2)\
                            , actual_service_date=datetime.now() - timedelta(days=20), extended_date=datetime.now() - timedelta(days=2))
        self.get_coupon_obj(unique_service_coupon='COUPON006', vin=product_obj, valid_days=30, valid_kms=3000\
                            , service_type=2, status=1, mark_expired_on=datetime.now() + timedelta(days=30)\
                            , actual_service_date=datetime.now() - timedelta(days=20), extended_date=datetime.now() + timedelta(days=30))
        self.get_coupon_obj(unique_service_coupon='COUPON007', vin=product_obj, valid_days=30, valid_kms=6000\
                            , service_type=3, status=1, mark_expired_on=datetime.now() + timedelta(days=60)\
                            , actual_service_date=datetime.now() - timedelta(days=20), extended_date=datetime.now() + timedelta(days=60))
    
    def test_get_sa_list(self):
        request = {'user': 'DEALER001'}
        sa_list = get_sa_list()
    
    
    
    
    
    
    
    