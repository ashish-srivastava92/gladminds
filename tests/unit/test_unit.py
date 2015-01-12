import os
import json

from django.conf import settings
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from django.test import TestCase
from datetime import datetime, timedelta
from unit.base_unit import RequestObject, GladmindsUnitTestCase
from gladminds.core.utils import get_coupon_info,\
 get_list_from_set, get_token, create_purchase_feed_data , \
 validate_otp, update_pass, format_date_string
from gladminds.bajaj import models
import boto
from gladminds.core.constants import FEEDBACK_TYPE, PRIORITY
from tastypie.test import TestApiClient
from integration.bajaj.base_integration import client
from gladminds.core.views.views import get_customer_info
        

class TestAssertWorks(TestCase):
    
    def test_assert_equals(self):
        self.assertEquals(100, 100, '100 == 100')
    
    def test_assert_true(self):
        self.assertTrue(100 > 1, '100 > 1')
          
class TestUtils(GladmindsUnitTestCase):
    
    def setUp(self):
        super(TestUtils, self).setUp()
        self.product_type_obj = self.get_product_type_obj(product_type='BIKE')
        self.dealer_obj = self.get_delear_obj(name='DEALER001')
        product_obj = self.get_product_obj(product_id="VINXXX001", product_type=self.product_type_obj, dealer_id=self.dealer_obj\
                                           , purchase_date=datetime.now(), customer_name='TestCustomer',
                                           customer_phone_number='+919999999', customer_id='SAP001')
        service_advisor = self.get_service_advisor_obj(service_advisor_id='SA001Test', name='UMOTO', phone_number='+914444861111')
        self.get_dealer_service_advisor_obj(dealer_id=self.dealer_obj, service_advisor_id=service_advisor, status='Y')
        self.get_coupon_obj(unique_service_coupon='COUPON005', product=product_obj, valid_days=30, valid_kms=500\
                            , service_type=1, status=4, mark_expired_on=datetime.now() - timedelta(days=2)\
                            , actual_service_date=datetime.now() - timedelta(days=20), extended_date=datetime.now() - timedelta(days=2))
        self.asc_user = User(username='ASC001')
        self.asc_user.set_password('123')
        self.asc_user.save()
        self.asc_user_profile = models.UserProfile(user=self.asc_user, phone_number="+911234567890")
        self.asc_user_profile.save()
        self.get_asc_obj(user=self.asc_user_profile, asc_id="ASC0001")
  
  
    def test_get_customer_info(self):  
        request=RequestObject(data={'vin':'12345678999'})
        product_info = models.ProductData(product_id = '12345678999', product_type=self.product_type_obj)
        product_info.save()
        result=get_customer_info(request.POST)
        self.assertEqual("VIN '12345678999' has no associated customer. Please register the customer.",result['message'])
        request = RequestObject(data={'vin':'123456789', 'current_user':'TestUser', 'groups':['dealers']})
        result = get_customer_info(request.POST)
        self.assertEqual("VIN '123456789' does not exist in our records. Please contact customer support: +91-9741775128.",
                                        result['message'])
        self.assertEqual("fail",result['status'])
        request = RequestObject(data={'vin':'VINXXX001', 'groups':['dealers']})
        result = get_customer_info(request.POST)
        self.assertEqual('+919999999', result['phone'])
            
    def test_get_coupon_info(self):  
        request = RequestObject(user='DEALER001', data={
                                'customerId': 'SAP001', 'vin': 'VINXXX001'}, file={'jobCard': ''})
        result = get_coupon_info(request.POST)
        self.assertEqual(30,result.valid_days)
    
    def test_save_pass(self):
        phone_number = '1234567890'
        password='1234'
        token = get_token(self.asc_user_profile, phone_number)
        self.assertTrue(isinstance(token, int))
        self.assertTrue(update_pass(token, password))
    
    def test_otp(self):
        phone_number = '1234567890'
        token = get_token(self.asc_user_profile, self.asc_user_profile.phone_number)
        self.assertTrue(isinstance(token, int))
        self.assertTrue(validate_otp(self.asc_user, token, phone_number))
              
    def test_format_date_string(self):
        date=format_date_string("20/07/1992")
        self.assertEqual(datetime, type(date)) 
           
    def test_create_feed_data(self):
        product_objs = self.get_product_obj(product_id="VINXXX0011", engine='manga')
        post_data = {'purchase-date':'07/08/1992','customer-phone':'7760814041','customer-name':'saurav'}
        temp_customer_id='123456'
        data = create_purchase_feed_data(post_data, product_objs, temp_customer_id)   
        self.assertEqual(data['vin'], 'VINXXX0011') 
           
    def test_get_list_from_set(self):
        data = get_list_from_set(FEEDBACK_TYPE)
        self.assertEqual(len(data), 4) 
        data = get_list_from_set(PRIORITY)
        self.assertEqual(len(data), 4) 
           
     
  
class TestFeedLogWithRemark(ResourceTestCase):
    '''
    '''
   
    def setUp(self):
        TestCase.setUp(self)
        self.api_client = client
        user = User.objects.create_user('gladminds', 'gladminds@gladminds.co',
                                         'gladminds')
        user.save()
   
    def test_remarks(self):
        
        file_path = os.path.join(settings.BASE_DIR,
                                 'tests/integration/bajaj/test_data/test_feed_log_remark.xml')
        xml_data = open(file_path, 'r').read()
        url = 'http://local.bajaj.gladminds.co:8000/api/v1/feed/?wsdl'
        
        self.api_client.post(url, data=xml_data,
                                    content_type='text/xml')
        feed_logs_obj = models.DataFeedLog.objects.all()
        self.assertEqual(len(feed_logs_obj), 1)

        file_name = feed_logs_obj[0].file_location.split("/")[-1]
           
           
        self.assertEqual(os.path.isfile("{0}/{1}".format(settings.BASE_DIR, file_name)), 
                         False, 'File should be deleted from local dir')
                                
        connection = boto.connect_s3(settings.S3_ID, settings.S3_KEY)
        s3_bucket = connection.get_bucket('gladminds')
                                
        file_uploaded_on_s3 = False
        for key in s3_bucket.list('aftersell/bajaj/feed-logs/dev'):
            uploaded_file = key.name.split("/")[-1]
            if uploaded_file == file_name:
                file_uploaded_on_s3=True 
        self.assertEqual(file_uploaded_on_s3, True, 'File is not Uploaded On S3')    
              