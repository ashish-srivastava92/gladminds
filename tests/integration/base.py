from tastypie.test import ResourceTestCase
from django.core import management
from django.contrib.auth.models import User, Group
from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common
from gladminds.management.commands import load_gm_migration_data
import os
from django.conf import settings
import json
from time import sleep
from datetime import datetime
from django.test import TestCase

from django.test.client import Client

client = Client()

__BACKOFF = [0.5, 1, 2, 4, 8, 16, 32, 64]


def _exponential_backoff(index):
    if index >= len(__BACKOFF):
        index = len(__BACKOFF) - 1
    if index < 0:
        index = 0
    return __BACKOFF[index]


def wait_for_sms(mobile, check_date=None, time_to_check_for=128):
    total_time = 0
    for i in range(10):
        #check for audit (use check date for filtering)
        if total_time > time_to_check_for:
            raise
        t = _exponential_backoff(i)
        total_time += t
        sleep(t)
    raise


class BaseTestCase(ResourceTestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.client = Client()
        load_email_obj = load_gm_migration_data.Command()
        load_email_obj.add_email_template()
        load_email_obj.add_sms_template()
        load_email_obj.add_group()

    def assert_successful_http_response(self, resp, msg=None):
        return self.assertTrue(resp.status_code >= 200 
                               and resp.status_code <= 299, msg)

    def assert_sms_received(self, mobile, check_date=datetime.now(), time_to_check_for=128, msg="sms failed"):
        try:
            wait_for_sms(mobile, check_date, time_to_check_for)
            return
        except:
            raise self.failureException(msg)

    def check_sms_sent(self, mobile):
        pass

    def check_service_type_of_coupon(self, id, service_type):
        pass

    def create_user(self):
        user = User.objects.create_user('gladminds', 'gladminds@gladminds.co', 'gladminds')
        user.save()
        return user

    def create_user_profile(self):
        user_obj = self.create_user()
        user_profile = aftersell_common.UserProfile(user=user_obj, phone_number="+91776084041")
        user_profile.save()
        return user_profile

    def create_dealer(self):
        test_user = User.objects.create_user('DEALER01', 'dealer@xyz.com', 'DEALER01@123')
        test_user.save()
        user_group = Group.objects.get(name='dealers')
        test_user.groups.add(user_group)

    def create_sdo(self):
        user_servicedesk_owner = User.objects.create_user(username='sdo', email='gm@gm.com', password='123')
        user_servicedesk_owner.save()
        user_group = Group.objects.get(name='SDO')
        user_servicedesk_owner.groups.add(user_group)
        user_profile = aftersell_common.UserProfile(user=user_servicedesk_owner, phone_number="+919999999999")
        user_profile.save()
        service_desk_owner = aftersell_common.ServiceDeskUser(user=user_profile, phone_number="+919999999999", email_id="srv.sngh@gmail.com", designation='SDO' )
        service_desk_owner.save()
        return user_profile

    def create_sdm(self):
        user_servicedesk_manager = User.objects.create_user(username='sdm', email='gm@gm.com', password='123')
        user_servicedesk_manager.save()
        user_group = Group.objects.get(name='SDM')
        user_servicedesk_manager.groups.add(user_group)
        user_profile = aftersell_common.UserProfile(user=user_servicedesk_manager, phone_number="+911999999989")
        user_profile.save()
        service_desk_owner = aftersell_common.ServiceDeskUser(user=user_profile, phone_number="+911999999989", email_id="srv.sngh@gmail.com", designation='SDM' )
        service_desk_owner.save()

    def create_service_advisor(self):
        user_serviceadvisor = User.objects.create_user(username='SA002Test', email='gm@gm.com', password='123')
        user_serviceadvisor.save()
        user_group = Group.objects.get(name='sas')
        user_serviceadvisor.groups.add(user_group)
        serviceadvisor_profile = aftersell_common.UserProfile(user=user_serviceadvisor, phone_number='+919999999998')
        serviceadvisor_profile.save()
        service_advisor_obj = aftersell_common.ServiceAdvisor(user=serviceadvisor_profile, service_advisor_id='SA002Test', name='UMOTOR', phone_number='+919999999998')
        service_advisor_obj.save()
        return service_advisor_obj

    def create_register_dealer(self):
        user_register_dealer = User.objects.create_user(username='RD002Test', email='gm@gm.com', password='123')
        user_register_dealer.save()
        user_group = Group.objects.get(name='dealers')
        user_register_dealer.groups.add(user_group)
        register_dealer_profile = aftersell_common.UserProfile(user=user_register_dealer, phone_number='+919999999997')
        register_dealer_profile.save()
        register_dealer_obj = aftersell_common.RegisteredDealer(user=register_dealer_profile, dealer_id ='RD002Test', role='dealer')
        register_dealer_obj.save()
        return register_dealer_obj

    def create_dealer_service_advisor(self):
        service_advisor1 = aftersell_common.ServiceAdvisor.objects.get(phone_number='+919999999998')
        dealer_obj = aftersell_common.RegisteredDealer.objects.get(dealer_id ='RD002Test')
        dealer_service_advisor_obj = aftersell_common.ServiceAdvisorDealerRelationship(dealer_id=dealer_obj, service_advisor_id=service_advisor1, status='Y')
        dealer_service_advisor_obj.save()
        return dealer_service_advisor_obj

    def dealer_login(self):
        self.create_dealer()
        self.client.login(username='DEALER01', password='DEALER01@123')

    def post_feedback(self):
        test_user = User.objects.create_user('DEALER02', 'dealer@xyz.com', 'DEALER01@123')
        test_user.save()
        user_group = Group.objects.get(name='dealers')
        test_user.groups.add(user_group)
        data = {'username': 'DEALER02', 'password': 'DEALER01@123'}
        response = client.post("/aftersell/dealer/login/", data=data)
        data = {"messsage":"test","priority":"High","advisorMobile":"+919999999998",
                "type":"Problem", "subject":"hello" }
        response = client.post("/aftersell/servicedesk/helpdesk", data=data)
        self.assertEqual(response.status_code, 200)

    def test_servicedesk_login_sdo(self):
        self.create_sdo()
        data = {'username': 'sdo', 'password': '123'}
        response = client.post("/aftersell/desk/login/", data=data)
        response = client.get("/aftersell/servicedesk/")
        self.assertEqual(response.status_code, 200)

    def test_servicedesk_login_sdm(self):
        self.create_sdm()
        data = {'username': 'sdm', 'password': '123'}
        response = client.post("/aftersell/desk/login/", data=data)
        response = client.get("/aftersell/servicedesk/")
        self.assertEqual(response.status_code, 200)

    def update_feedback_assigned(self):
        self.create_sdo()
        data = {"Assign_To":"+919999999999","status":"Open","Priority":"High", "comments":"ssss", "rootcause":"ssss", "resolution":"ssssss"  }
        response = client.post("/aftersell/feedbackdetails/1/", data=data)
        self.assertEqual(response.status_code, 200)

    def update_feedback_resolved(self):
        self.create_sdm()
        data = {"Assign_To":"+919999999999","status":"Resolved","Priority":"High", "comments":"ssss", "rootcause":"ssss", "resolution":"ssssss"  }
        response = client.post("/aftersell/feedbackdetails/1/", data=data)
        self.assertEqual(response.status_code, 200)

    def update_feedback_fields(self):
        self.create_sdo()
        data = {"Assign_To":"None","status":"Closed","Priority":"High","comments":"ssss","rootcause":"ssss", "resolution":"ssssss" }
        response = client.post("/aftersell/feedbackdetails/1/", data=data)
        self.assertEqual(response.status_code, 200)


    def get_product_details(self, **kwargs):
        product_data_obj = common.ProductData.objects.get(**kwargs)
        return product_data_obj

    def register_customer(self):
        data = {
                    'customer-phone': '9999999999',
                    'customer-name': 'TestUser',
                    'purchase-date': '11/5/2014',
                    'customer-vin': 'XXXXXXXXXX',
                    'customer-id': 'GMCUSTOMER01',
                }
        response = self.client.post('/aftersell/register/customer', data=data)
        print response.status_code
        return response

    def send_dispatch_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')

    def send_asc_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/asc_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assert_successful_http_response(response)

    def check_asc_feed_saved_to_db(self):
        self.send_asc_feed()
        asc = aftersell_common.RegisteredDealer.objects.get(dealer_id='ASC001')
        self.assertEquals('ASC001', asc.dealer_id)

    def check_asc_exists(self, name, check_name, by):
        self.asc_data = {
                    'name' : 'test_asc',
                    'address' : 'ABCDEF',
                    'password' : '123',
                    'phone-number' : '9999999999',
                    'email' : 'abc@abc.com',
                    'pincode' : '562106'
                }
        if by == 'dealer':
            response = self.client.post('/aftersell/register/asc', data=self.asc_data)
            self.assertEqual(response.status_code, 200)
        elif by == 'self':
            response = self.client.post('/aftersell/asc/self-register/', data=self.asc_data)
            self.assertEqual(response.status_code, 200)

        temp_asc_obj = self.get_temp_asc_obj(name=name)
        self.assertEqual(temp_asc_obj.name, check_name)

    def send_purchase_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_purchase_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')



        