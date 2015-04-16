from smoke.utility import UtilityResourceTest
from integration.core.constants import BajajUrls, Constants, COUPON_SCHEMA
from integration.core.constants import COUPON_DISPATCH_XML_DATA, COUPON_PURCHASE_XML_DATA


class TestBajajCouponDataApi(UtilityResourceTest):
    def setUp(self):
        super(TestBajajCouponDataApi, self).setUp()
        self.send_dispatch_feed(xml_data=COUPON_DISPATCH_XML_DATA)
        self.send_purchase_feed(xml_data=COUPON_PURCHASE_XML_DATA)

    def test_couponcheck(self):
        phone_number="9999999999"
        self.check_coupon_open('USC2917')
        data = 'A {0} {1} {2}'.format('TM-2912270', 450, 1)
        self.check_coupon(phone_number, data)
        self.check_coupon_inprogress('USC2917')
    
    def test_close_coupon(self):
        phone_number="9999999999"
        self.check_coupon_inprogress('USC2917')
        data = 'C {0} {1}'.format('TM-2912270', 'USC2917')
        self.check_coupon(phone_number, data)
        self.check_coupon_closed('USC2917') 
    
    def test_close_opened_coupon(self): 
        phone_number="9999999999"
        self.check_coupon_open('USC2927')
        data = 'C {0} {1}'.format('TM-2912270', 'USC2927')
        self.check_coupon_false(phone_number, data)
    
    def test_wrong_UCN_close_coupon(self):
        phone_number="9999999999"
        data = 'A {0} {1} {2}'.format('TM-2912270', 7990, 2)
        self.check_coupon(phone_number, data)
        self.check_coupon_inprogress('USC2927')
        data = 'C {0} {1}'.format('TM-2912270', 'USC297')
        self.check_coupon_false(phone_number, data)
    
    def test_wrong_ID_close_coupon(self):
        phone_number="9999999999"
        data = 'A {0} {1} {2}'.format('TM-2912270', 7990, 2)
        self.check_coupon(phone_number, data)
        self.check_coupon_inprogress('USC2927')
        data = 'C {0} {1}'.format('TM-291220', 'USC2927')
        self.check_coupon_false(phone_number, data)
        
        
    def test_check_exceed_limit(self):         
        phone_number="9999999999"
        data = 'A {0} {1} {2}'.format('TM-2912270', 8500, 2, )
        self.check_coupon(phone_number, data)
        self.check_coupon_exceed_limit('USC2927')
    
    def test_progress_exeeded_coupon(self):
        phone_number="9999999999"
        data = 'A {0} {1} {2}'.format('TM-2912270', 7500, 2, )
        self.check_coupon(phone_number, data)
        self.check_coupon_inprogress('USC2927')
    
    def test_progress_next_already_one_inprogress(self):
        phone_number="9999999999"
        self.check_coupon_inprogress('USC2927')
        self.check_coupon_open('USC2937')
        data = 'A {0} {1} {2}'.format('TM-2912270',7000, 3)
        self.check_coupon(phone_number, data)
        self.check_coupon_open('USC2937')
        self.check_coupon_inprogress('USC2927')