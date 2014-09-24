from django.contrib.auth.models import User
from django.test.client import Client
from tastypie.test import ResourceTestCase, TestApiClient
from provider.oauth2.models import AccessToken
from provider.oauth2.models import Client as auth_client
from test_constants import GM_USER, GM_PRODUCTS, GM_COUPONS
client = TestApiClient()
djangoClient=Client()


class GladMindsApiTests(ResourceTestCase):

    def setUp(self):
        super(GladMindsApiTests, self).setUp()
        self.access_token = 'testaccesstoken'
        user = User.objects.create_user(username='gladminds', email='gm@gm.com',password='gladminds')
        secret_cli = auth_client(user=user, name='client', client_type=1, url='')
        secret_cli.save()
        access = AccessToken(user=user, token=self.access_token, client=secret_cli)
        access.save()

    def add_a_gmuser(self):
        uri = '/v1/gmusers/'
        resp = self.api_client.post(uri, format='json', data=GM_USER)
        return resp

    def add_a_product(self):
        uri = '/v1/products/'
        resp = self.api_client.post(uri, format='json', data=GM_PRODUCTS)
        return resp

    def add_a_coupon(self):
        uri = '/v1/coupons/'
        resp = self.api_client.post(uri, format='json', data=GM_COUPONS)
        return resp

    def test_create_a_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)

    def test_get_a_particular_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/gmusers/1/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        self.assertEqual(len(self.deserialize(resp)), 19)
    
    def test_update_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/gmusers/1/', format='json')
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        resp = self.api_client.put('/v1/gmusers/1/', format='json', data={"phone_number":"1234512345"})
        self.assertEquals(resp.status_code, 200)
        resp = self.api_client.get('/v1/gmusers/1/', format='json')
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234512345")
    
    def test_delete_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/gmusers/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        resp = self.api_client.delete('/v1/gmusers/1/', format='json')
        self.assertEquals(resp.status_code,204)

    def test_create_a_product(self):
        resp = self.add_a_product()
        self.assertEquals(resp.status_code,201)

    def test_get_a_particular_product(self):
        resp = self.add_a_product()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/products/1/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['vin'], "22")
        self.assertEqual(len(self.deserialize(resp)), 23)

    def test_update_a_product(self):
        resp = self.add_a_product()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/products/1/', format='json')
        self.assertEqual(self.deserialize(resp)['vin'], "22")
        resp = self.api_client.put('/v1/products/1/', format='json', data={"vin":"11"})
        resp = self.api_client.get('/v1/products/1/', format='json')
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.deserialize(resp)['vin'], "11")

    def test_delete_product(self):
        resp = self.add_a_product()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/products/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        resp = self.api_client.delete('/v1/products/1/', format='json')
        self.assertEquals(resp.status_code,204)

    def test_create_a_coupon(self):
        resp = self.add_a_coupon()
        self.assertEquals(resp.status_code,201)

    def test_get_a_particular_coupon(self):
        resp = self.add_a_coupon()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/coupons/1/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['unique_service_coupon'], '1')
        self.assertEqual(len(self.deserialize(resp)), 18)

    def test_update_a_coupon(self):
        resp = self.add_a_coupon()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/coupons/1/', format='json')
        self.assertEqual(self.deserialize(resp)['unique_service_coupon'], '1')
        resp = self.api_client.put('/v1/coupons/1/', format='json', data={"unique_service_coupon":'2'})
        self.assertEquals(resp.status_code, 200)
        resp = self.api_client.get('/v1/coupons/1/', format='json')
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.deserialize(resp)['unique_service_coupon'], '2')

    def test_delete_coupon(self):
        resp = self.add_a_coupon()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/coupons/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        resp = self.api_client.delete('/v1/coupons/1/', format='json')
        self.assertEquals(resp.status_code,204)
