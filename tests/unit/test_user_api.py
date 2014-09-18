# import datetime
# from django.contrib.auth.models import User
# from tastypie.test import ResourceTestCase
# from django.utils.text import slugify
# from gladminds.models import common
# 
# class GladMindUserResourceTest(ResourceTestCase):
#     
#     def setUp(self):
#         super(GladMindUserResourceTest, self).setup()
#     
#     def test_get_a_paticular_gmuser(self):
#         resp = self.api_client.get('v1/gmusers/?phone_number=8983567622', format='json')
#         self.assertValidJSONResponse(resp)
#         self.assertEqual(len(self.deserialize(resp)['objects']), 1)