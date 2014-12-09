from gladminds.bajaj import models
from gladminds.default import models as gm_models
from gladminds.afterbuy import models as afterbuy_models
from integration.bajaj.base import BaseTestCase
import datetime
from django.test.client import Client

client = Client(SERVER_NAME='bajaj')


class System(BaseTestCase):
    def __init__(self, tester):
        self.tester = tester

    def create_gladmind_user(self):
        user_obj = self.create_user(username='glad', email='gm@gm.com', password='gladminds',phone_number='+9199999998')
        glad_obj = models.UserProfile(user=user_obj, phone_number='+9199999998')
        glad_obj.save()
        return glad_obj

    def get_brand_info(self, **kwargs):
        brand_obj = gm_models.Brand.objects.get(**kwargs)
        return brand_obj

    def get_product_info(self, **kwargs):
        product_data = models.ProductData.objects.get(**kwargs)
        return product_data

    def create_and_get_product_insurance_info(self, **kwargs):
        product_insurance = afterbuy_models.ProductInsuranceInfo(**kwargs)
        product_insurance.save()
        return product_insurance

    def create_and_get_product_warranty_info(self, **kwargs):
        product_warranty = afterbuy_models.ProductWarrantyInfo(**kwargs)
        product_warranty.save()
        return product_warranty

    def create_and_get_spare_data(self, **kwargs):
        spare_data = models.SparesData(**kwargs)
        spare_data.save()
        return spare_data

    def create_sdo(self, **kwargs):
        user_servicedesk_owner_profile = self.create_user(username=kwargs['username'], email=kwargs['email'], password=kwargs['password'], group_name='SDO', phone_number=kwargs['phone_number'])
        user_servicedesk_owner = models.ServiceDeskUser(user_profile=user_servicedesk_owner_profile)
        user_servicedesk_owner.save()
        return user_servicedesk_owner

    def create_sdm(self, **kwargs):
        user_servicedesk_manager_profile = self.create_user(username=kwargs['username'], email=kwargs['email'], password=kwargs['password'], group_name='SDM', phone_number=kwargs['phone_number'])
        user_servicedesk_manager = models.ServiceDeskUser(user_profile=user_servicedesk_manager_profile)
        user_servicedesk_manager.save()
        return user_servicedesk_manager
    
    def create_sla(self, **kwargs):
        sla_object = models.SLA(priority=kwargs['priority'], response_time=2,response_unit='mins', reminder_time=2, reminder_unit='hrs', resolution_time=10, resolution_unit='days')
        sla_object.save()
        
    def get_temp_customer_obj(self, **kwargs):
        temp_customer_obj = models.CustomerTempRegistration.objects.get(**kwargs)
        return temp_customer_obj

    def dealer_login(self):
        self.create_user(username='DEALER01', email='dealer@xyz.com', password='DEALER01@123', group_name='dealers', phone_number="+91776084042")
        data = {'username': 'DEALER01', 'password': 'DEALER01@123'}
        self.tester.client.login(username='DEALER01', password='DEALER01@123')

    def post_feedback(self):
        data = {'username': 'GMDEALER001', 'password': 'GMDEALER001@123'}
        response = client.post("/aftersell/dealer/login/", data=data)
        self.tester.assertEqual(response.status_code, 302)
        data = {"description":"test","advisorMobile":"+919999999999",
                "type":"Problem", "summary":"hello" }
        response = client.post("/aftersell/servicedesk/helpdesk", data=data)
        self.tester.assertEqual(response.status_code, 200)

    def login(self, **kwargs):
        create_mock_data = {'username': kwargs['username'], 'password': kwargs['password']}
        response = client.post("/aftersell/"+ kwargs['provider'] +"/login/", data=create_mock_data)
        self.tester.assertEqual(response.status_code, 302)

    def get_feedback_information(self):
        response = client.get("/aftersell/servicedesk/")
        self.tester.assertEqual(response.status_code, 200)

    def update_feedback(self, **kwargs):
        data = {"assign_to":"+91000000000",
                "status":"Open","Priority":"High",
                "comments":"testing", "rootcause":"testing",
                "resolution":"testing", "reporter_status": False, "due_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if kwargs.get('status'):
            data['status'] = kwargs['status']
        if kwargs.get('assign_To'):
            data['assign_To'] = kwargs['assign_To']
        response = client.post("/aftersell/feedbackdetails/1/", data=data)
        self.tester.assertEqual(response.status_code, 200)

    def get_product_details(self, **kwargs):
        product_data_obj = models.ProductData.objects.get(**kwargs)
        return product_data_obj

    def register_customer(self):
        data = {
                    'customer-phone': '9999999999',
                    'customer-name': 'TestUser',
                    'purchase-date': '11/5/2014',
                    'customer-vin': 'XXXXXXXXXX',
                    'customer-id': 'GMCUSTOMER01',
                }
        response = self.tester.client.post('/aftersell/register/customer', data=data)
        self.tester.assertEqual(response.status_code, 200)

    def get_temp_asc_obj(self, **kwargs):
        temp_asc_obj = models.ASCTempRegistration.objects.get(**kwargs)
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
            response = self.tester.client.post('/aftersell/register/asc', data=self.asc_data)
            self.tester.assertEqual(response.status_code, 200)
        elif by == 'self':
            response = self.tester.client.post('/aftersell/asc/self-register/', data=self.asc_data)
            self.tester.assertEqual(response.status_code, 200)

        temp_asc_obj = self.get_temp_asc_obj(name=name)
        self.tester.assertEqual(temp_asc_obj.name, check_name)

    def verify_result(self, **kwargs):
        self.tester.assertEquals(kwargs['input'], kwargs['output'])

#########################################send feed function################################################################


