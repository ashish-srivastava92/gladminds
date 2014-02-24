from suds.client import Client
from suds.transport.http import HttpAuthenticated
import logging
logger = logging.getLogger("gladminds")

class BaseExportFeed(object):
    def __init__(self, username=None, password = None, wsdl_url = None):
        self.username = username
        self.password = password
        self.wsdl_url = wsdl_url
    
    def get_http_authenticated(self):
         return HttpAuthenticated(username=self.username, password=self.password)
    
    def get_client(self):
        transport = HttpAuthenticated(username=self.username, password=self.password)
        return Client(url = self.wsdl_url, transport=transport)

class ExportCouponRedeemFeed(BaseExportFeed):    
    def export(self, items=None, item_batch=None):
        logger.info("Export coupon data: Items:{0} and Item_batch: {1}".format(items, item_batch))
        client = self.get_client()
        result = client.service.MI_GCP_UCN_Sync(ITEM=items, ITEM_BATCH=item_batch)
        logger.info("Response from SAP: {0}".format(result))
        
        
        
        
        
         