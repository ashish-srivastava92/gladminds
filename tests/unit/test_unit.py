from unittest import TestCase
from datetime import datetime, timedelta
from gladminds.utils import get_sa_list, get_coupon_info, get_customer_info
from unit.base_unit import RequestObject, GladmindsUnitTestCase

class TestAssertWorks(TestCase):

    def test_assert_equals(self):
        self.assertEquals(100, 100, '100 == 100')

    def test_assert_true(self):
        self.assertTrue(100 > 1, '100 > 1')

class TestUtils(GladmindsUnitTestCase):
    
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
        self.get_coupon_obj(unique_service_coupon='COUPON005', vin=product_obj, valid_days=30, valid_kms=500\
                            , service_type=1, status=4, mark_expired_on=datetime.now() - timedelta(days=2)\
                            , actual_service_date=datetime.now() - timedelta(days=20), extended_date=datetime.now() - timedelta(days=2))
        self.get_message_template(template_key='SEND_CUSTOMER_VALID_COUPON'\
                                  ,template='Service Type {service_type}. UCN {coupon}.', description='Desc')

    def test_get_sa_list(self):
        request = RequestObject(user='DEALER001', data={'customerId': 'SAP001', 'vin': 'VINXXX001'}, file={'jobCard': ''})
        sa_list = get_sa_list(request)
        self.assertEqual(len(sa_list), 1)
        coupon_info=get_coupon_info(request)
        self.assertEqual(coupon_info.keys(), ['status', 'message'])
        customer = get_customer_info(request)
        self.assertEquals(customer.keys(), ['customer_phone', 'customer_id'])
    
    
    
    
    
    
    