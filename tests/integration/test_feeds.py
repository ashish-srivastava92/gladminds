import logging
logger = logging.getLogger("gladminds")
from base_integration import GladmindsResourceTestCase
from gladminds.models import common
from suds.client import Client
import xml.etree.ElementTree as ET

class FeedsResourceTest(GladmindsResourceTestCase):

    def setUp(self):
        super(FeedsResourceTest, self).setUp()

    def test_service_advisor_feed(self):

        #url = '/api/v1/bajaj/feed/?wsdl'
        #client = Client(url)
        #result = Client.service.MI_GCP_UCN_Sync(ITEM=items, ITEM_BATCH=item_batch)

        #tree = ET.parse('service_advisor_feed.xml')
        wsdl = open('service_advisor_feed.xml','r').read()

        self.assertHttpCreated(self.api_client.post(uri='/api/v1/bajaj/feed/?wsdl', data=wsdl))
#         dealer_data = common.GladMindUsers.objects(dealer_id='dealer12')
#         service_advisor_obj = common.ServiceAdvisor.objects.get(dealer_id=dealer_data, service_advisor_id="2231311")
#         self.assertEquals(service_advisor_obj.status, "active", "Service Advisor status should be active")


