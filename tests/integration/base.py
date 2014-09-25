from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User, Group
from gladminds.models import common
import xml.etree.ElementTree as ET
from django.db import transaction
from gladminds.aftersell.models import common as aftersell_common
from gladminds.afterbuy.models import common as afterbuy_common
from gladminds.management.commands import load_gm_migration_data
import os
from django.conf import settings
from time import sleep
from django.test import TestCase
from gladminds.core import feed
from datetime import datetime, timedelta
from provider.oauth2.models import Client as auth_client
from provider.oauth2.models import AccessToken

from django.test.client import Client
from django.template.base import kwarg_re

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
        super(BaseTestCase, self).setUp()
        self.client = Client()
        self.access_token = 'testaccesstoken'
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

    def create_user(self, **kwargs):
        user = User.objects.create_user(kwargs['username'], kwargs['email'], kwargs['password'])
        user.save()
        if kwargs.get('group_name'):
            user_group = Group.objects.get(name=kwargs['group_name'])
            user.groups.add(user_group)
        if kwargs.get('group_name'):
            user_profile = aftersell_common.UserProfile(user=user, phone_number=kwargs['phone_number'])
            user_profile.save()
            return user_profile

    def get_user_obj(self, **kwargs):
        user_obj = User.objects.get(**kwargs)
        return user_obj

    def create_gladmind_user(self):
        user_obj = self.create_user(username='glad', email='gm@gm.com', password='gladminds',phone_number='+9199999998')
        glad_obj = common.GladMindUsers(user=user_obj, phone_number='+9199999998')
        glad_obj.save()
        glad_user_obj = common.GladMindUsers.objects.get(phone_number='+9199999998')
        self.assertEqual(glad_user_obj.phone_number, '+9199999998')
        return glad_user_obj

    def create_get_brand_obj(self, **kwargs):
        brand_obj = common.BrandData(**kwargs)
        brand_obj.save()
        return brand_obj

    def create_get_product_type_obj(self, **kwargs):
        product_type_data_obj = common.ProductTypeData(**kwargs)
        product_type_data_obj.save()
        return product_type_data_obj

    def create_get_user_product_obj(self, **kwargs):
        user_project_obj = afterbuy_common.UserProducts(**kwargs)
        user_project_obj.save()
        return user_project_obj

    def create_get_product_obj(self, **kwargs):
        product_data = common.ProductData(**kwargs)
        product_data.save()
        return product_data

    def create_get_product_insurance_info(self, **kwargs):
        product_insurance = common.ProductInsuranceInfo(**kwargs)
        product_insurance.save()
        return product_insurance

    def create_get_product_warranty_info(self, **kwargs):
        product_warranty = common.ProductWarrantyInfo(**kwargs)
        product_warranty.save()
        return product_warranty

    def create_get_spare_data(self, **kwargs):
        spare_data = common.SparesData(**kwargs)
        spare_data.save()
        return spare_data

    def create_dealer(self):
        self.create_user(username='DEALER01', email='dealer@xyz.com', password='DEALER01@123', group_name='dealers', phone_number="+91776084042")
        user_profile_obj = aftersell_common.UserProfile.objects.get(phone_number="+91776084042")
        self.assertEqual(user_profile_obj.phone_number, '+91776084042')

    def create_sdo(self):
        user_servicedesk_owner = self.create_user(username='sdo', email='gm@gm.com', password='123', group_name='SDO', phone_number="+919999999999")
        service_desk_owner = aftersell_common.ServiceDeskUser(user=user_servicedesk_owner, phone_number="+919999999999", email_id="srv.sngh@gmail.com", designation='SDO' )
        service_desk_owner.save()
        service_desk_owner_obj = aftersell_common.ServiceDeskUser.objects.get(designation='SDO')
        self.assertEqual(service_desk_owner_obj.designation, 'SDO')
        return service_desk_owner

    def create_sdm(self):
        user_servicedesk_manager = self.create_user(username='sdm', email='gm@gm.com', password='123', group_name='SDM', phone_number="+911999999989")
        service_desk_owner = aftersell_common.ServiceDeskUser(user=user_servicedesk_manager, phone_number="+911999999989", email_id="srv.sngh@gmail.com", designation='SDM' )
        service_desk_owner.save()
        service_desk_owner_obj = aftersell_common.ServiceDeskUser.objects.get(designation='SDM')
        self.assertEqual(service_desk_owner_obj.designation, 'SDM')

    def create_service_advisor(self):
        user_serviceadvisor = self.create_user(username='SA002Test', email='gm@gm.com', password='123', group_name='sas', phone_number='+919999999998')
        service_advisor_obj = aftersell_common.ServiceAdvisor(user=user_serviceadvisor, service_advisor_id='SA002Test', name='UMOTOR', phone_number='+919999999998')
        service_advisor_obj.save()
        service_advisor = aftersell_common.ServiceAdvisor.objects.get(service_advisor_id='SA002Test')
        self.assertEqual(service_advisor.service_advisor_id, 'SA002Test')
        return service_advisor_obj

    def create_register_dealer(self):
        user_register_dealer = self.create_user(username='RD002Test', email='gm@gm.com', password='123', group_name='dealers', phone_number='+919999999997')
        register_dealer_obj = aftersell_common.RegisteredDealer(user=user_register_dealer, dealer_id ='RD002Test', role='dealer')
        register_dealer_obj.save()
        register_dealer = aftersell_common.RegisteredDealer.objects.get(dealer_id='RD002Test')
        self.assertEqual(register_dealer.dealer_id, 'RD002Test')
        return register_dealer_obj

    def create_dealer_service_advisor(self):
        service_advisor1 = aftersell_common.ServiceAdvisor.objects.get(phone_number='+919999999998')
        dealer_obj = aftersell_common.RegisteredDealer.objects.get(dealer_id ='RD002Test')
        dealer_service_advisor_obj = aftersell_common.ServiceAdvisorDealerRelationship(dealer_id=dealer_obj, service_advisor_id=service_advisor1, status='Y')
        dealer_service_advisor_obj.save()
        dealer_service_advisor = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(status='Y')
        self.assertEqual(dealer_service_advisor .status, 'Y')
        return dealer_service_advisor_obj

    def get_temp_customer_obj(self, **kwargs):
        temp_customer_obj = common.CustomerTempRegistration.objects.get(**kwargs)
        return temp_customer_obj

    def dealer_login(self):
        self.create_dealer()
        self.client.login(username='DEALER01', password='DEALER01@123')

    def post_feedback(self):
        self.create_dealer()
        data = {'username': 'DEALER01', 'password': 'DEALER01@123'}
        response = client.post("/aftersell/dealer/login/", data=data)
        self.assertEqual(response.status_code, 302)
        data = {"messsage":"test","priority":"High","advisorMobile":"+919999999998",
                "type":"Problem", "subject":"hello" }
        response = client.post("/aftersell/servicedesk/helpdesk", data=data)
        self.assertEqual(response.status_code, 200)

    def servicedesk_login_sdo(self):
        self.create_sdo()
        data = {'username': 'sdo', 'password': '123'}
        response = client.post("/aftersell/desk/login/", data=data)
        self.assertEqual(response.status_code, 302)
        response = client.get("/aftersell/servicedesk/")
        self.assertEqual(response.status_code, 200)

    def servicedesk_login_sdm(self):
        self.create_sdm()
        data = {'username': 'sdm', 'password': '123'}
        response = client.post("/aftersell/desk/login/", data=data)
        self.assertEqual(response.status_code, 302)
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
        self.assertEqual(response.status_code, 200)
        return response

    def send_dispatch_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(response.status_code, 200)

    def send_dispatch_feed_without_ucn(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed_without_ucn.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)

    def send_asc_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/asc_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assert_successful_http_response(response)

    def check_asc_feed_saved_to_db(self):
        self.send_asc_feed()
        asc = aftersell_common.RegisteredDealer.objects.get(dealer_id='ASC001')
        self.assertEquals('ASC001', asc.dealer_id)

    def send_service_advisor_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(response.status_code, 200)

    def send_service_advisor_feed_with_new_status(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed_2.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)

    def check_service_feed_saved_to_db(self):
        self.assertEquals(3, aftersell_common.RegisteredDealer.objects.count())
        dealer_data = aftersell_common.RegisteredDealer.objects.all()[0]
        self.assertEquals(u"GMDEALER001", dealer_data.dealer_id)
        service_advisors = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')
        self.assertEquals(1, len(service_advisors))
        self.assertEquals(u"GMDEALER001SA01", service_advisors[0].service_advisor_id)

    def check_service_advisor_dealer_relationship_db(self):
        sa_dealer_rel_data = aftersell_common.ServiceAdvisorDealerRelationship.objects.all()
        self.assertEquals(3, len(sa_dealer_rel_data))
        self.assertEquals(3, aftersell_common.ServiceAdvisor.objects.count())
        sa_obj_1 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')
        dealer_obj_1 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER001')
        sa_dealer_rel_obj_1 = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_1[0], dealer_id=dealer_obj_1[0])
        self.assertEquals('Y', sa_dealer_rel_obj_1.status)
        sa_obj_2 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA02')
        dealer_obj_2 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER002')
        sa_dealer_rel_obj_2 = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_2[0], dealer_id=dealer_obj_2[0])
        self.assertEquals('Y', sa_dealer_rel_obj_2.status)

    def check_data_saved_to_db(self):
        sa_obj_1 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')
        self.assertEquals('+9155555', sa_obj_1[0].phone_number)
        dealer_obj_1 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER001')
        sa_dealer_rel_obj_1 = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_1[0], dealer_id=dealer_obj_1[0])
        self.assertEquals('N', sa_dealer_rel_obj_1.status)
        sa_obj_2 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA02')
        dealer_obj_2 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER002')
        sa_dealer_rel_obj_2 = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_2[0], dealer_id=dealer_obj_2[0])
        self.assertEquals('Y', sa_dealer_rel_obj_2.status)

    def send_purchase_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_purchase_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

    def send_purchase_feed_with_diff_cust_num(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/purchase_feed_with_diff_cust_num.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)

    def check_for_auth(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/feeds_for_testing_auth.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

    def  send_as_feed_without_id(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/without_sa_id_sa_feed.xml')
        xml_data = open(file_path, 'r').read()
        with transaction.atomic():
            response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
            self.assertEqual(200, response.status_code)

        response_content = response.content
        xml_parser = ET.fromstring(response_content)
        with transaction.atomic():
            status = xml_parser.findall('*//{http://api.gladmindsplatform.co/api/v1/bajaj/feed/}postDealerResult')[0].text
            self.assertEqual(status, 'SUCCESS')

    def send_sa_upate_mobile_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/SA_mobile_update_data/SA_update_mobile_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)

    def coupon_data_db(self):
        self.assertEqual(common.CouponData.objects.count(), 2, "Two coupon created")
        coupon_data = common.CouponData.objects.filter(unique_service_coupon='USC001')[0]
        self.assertEquals(u"USC001", coupon_data.unique_service_coupon)
        coupon_data.status = 2
        coupon_data.closed_date = datetime.now()
        coupon_data.actual_service_date = datetime.now()
        coupon_data.save()

        today = datetime.now()
        start_date = today - timedelta(days=1)
        end_date = today
        redeem_obj = feed.CouponRedeemFeedToSAP()
        feed_export_data = redeem_obj.export_data(start_date=start_date, end_date=end_date)

        self.assertEqual(len(feed_export_data[0]), 1, "Not accurate length of feeds log")
        self.assertEqual(feed_export_data[0][0]["GCP_UCN_NO"], u'USC001', "Not accurate UCN")

    def check_product_data_db(self):
        self.assertEquals(1, common.ProductData.objects.count())
        product_data = common.ProductData.objects.all()[0]
        self.assertEquals(u"XXXXXXXXXX", product_data.vin)
        self.assertEquals(2, common.CouponData.objects.count())
        coupon_data = common.CouponData.objects.all()[0]
        self.assertEquals(u"USC001", coupon_data.unique_service_coupon)

    def service_advisor_db_upadted(self):
        sa_obj_1 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')
        dealer_obj_1 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER001')
        self.assertEquals('+9112345', sa_obj_1[0].phone_number)
        sa_dealer_rel_obj_2 =  aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_1[0], dealer_id=dealer_obj_1[0])
        self.assertEquals('N', sa_dealer_rel_obj_2.status)
        sa_obj_2 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA02')
        dealer_obj_2 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER002')
        self.assertEquals('+91555551', sa_obj_2[0].phone_number)
        dealer_obj_3 =  aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER003')
        sa_obj_3 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA03')
        self.assertEquals(0, len(sa_obj_3))
        self.assertEquals(0, len(dealer_obj_3))

    def get_temp_asc_obj(self, **kwargs):
        temp_asc_obj = aftersell_common.ASCSaveForm.objects.get(**kwargs)
        return temp_asc_obj

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


        