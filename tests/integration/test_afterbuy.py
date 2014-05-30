''' Test Case for testing out the Afterbuy Api
'''

from integration.base_integration import GladmindsResourceTestCase
from django.test.client import Client
from gladminds.models import common

client = Client()


class TestAfterbuy(GladmindsResourceTestCase):

    def setUp(self):
        pass
        

    def test_create_new_user(self):
        '''
            Response of Api Status :
                {
                "status": 1, 
                "username": "testuser", 
                "sourceURL": "", 
                "thumbURL": "", 
                "message": "Success!", 
                "id": "GMS176DAE19163F", 
                "unique_id": "GMS176DAE19163F"
                }
        '''
        data = {
            'txtState': 'Uttar Pradesh',
            'txtCountry': 'india',
            'txtMobile': '99999999',
            'txtPassword': 'password',
            'txtEmail': 'email@dsdsdsds.com',
            'txtAddress': 'bangalore',
            'btn_reg_submit': 'submit',
            'txtConfirmPassword': 'password',
            'action': 'newRegister',
            'picImgURL': 'df',
            'profilePIC': '',
            'txtName': 'testuser'
        }
        response = client.post('/afterbuy/', data=data)
        print "%%%%%%%%",response.status_code, response.content
        print common.GladMindUsers.objects.all()
        

    def test_check_login(self):
        self.test_create_new_user()
        data = { 
                    'action': 'checkLogin', 
                    'txtPassword': 'password', 
                    'txtUsername': 'testuser'
                }
        response = client.post(
            '/afterbuy/', data =data)

        print response
        raise
    
    
    def test_product_details(self):
        client.get('/afterbuy/', data={'action': 'getProducts'})
        

    def test_create_item(self):
        client.get('/afterbuy/', data={'action': 'addingItem'})
