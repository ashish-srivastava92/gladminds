import logging
import datetime
from django.test import TestCase
from django.utils import unittest

from integration.bajaj.base import BaseTestCase
from integration.bajaj.test_brand_logic import Brand
from integration.bajaj.test_system_logic import System

logger = logging.getLogger('gladminds')

class CTSResourceTest(BaseTestCase):
    multi_db=True

    def setUp(self):
        TestCase.setUp(self)
        self.brand = Brand(self)
        self.system = System(self)
        BaseTestCase.setUp(self)
        self.create_user(username='bajaj', email='bajaj@gladminds.co', password='bajaj', is_superuser=True)
        self.brand.send_container_tracker_feed()
        self.access_token = self.brand.admin_login()

    def test_get_container_indent(self):
        '''
           Test the GET container indent data based on logged in user
           1. Admin sees all the Indents
           2. Transporters see only Indents under him
        '''
        brand = self.brand
        system = self.system
        admin_access_token=self.access_token
        
        saved_cts_indent_data=brand.get_container_indent(admin_access_token)
        system.verify_result(input=len(saved_cts_indent_data), output=2)
        
        tranporter_access_token=brand.tranporter_login()
        saved_cts_indent_data=brand.get_container_indent(tranporter_access_token)
        system.verify_result(input=len(saved_cts_indent_data), output=1)

    def test_submit_indent(self):
        '''
           Test to change status of an indent to Inprogress and
           update modified date
        '''
        brand = self.brand
        system = self.system
        admin_access_token=self.access_token
        
        saved_cts_indent_data=brand.get_container_indent(admin_access_token)
        system.verify_result(input=saved_cts_indent_data[0]['status'], output='Open')
        
        indent_id=saved_cts_indent_data[0]['id']
        brand.submit_container_indent(admin_access_token, str(indent_id))
        
        saved_cts_indent_data=brand.get_container_indent(admin_access_token)
        system.verify_result(input=saved_cts_indent_data[0]['status'], output='Inprogress')
        
        posted_modified_date=datetime.datetime.strptime('2015-07-02', '%Y-%m-%d')
        saved_modified_date=datetime.datetime.strptime(saved_cts_indent_data[0]['modified_date'], '%Y-%m-%dT%H:%M:%S')
        system.verify_result(input=saved_modified_date, output=posted_modified_date)

    def test_get_indent_status_count(self):
        '''
           Test the GET container Indent count based on status
           1. super admin sees all the indents thus 1 Open and 1 Inprogress
           2. Tranporter sees only his indents thus only 1 Open indent
        '''
        brand = self.brand
        system = self.system
        admin_access_token=self.access_token
        
        cts_indent_count=brand.get_indent_count(admin_access_token)
        system.verify_result(input=len(cts_indent_count), output=2)
        
        open_count = filter(lambda active: active['status'] == 'Inprogress', cts_indent_count)
        system.verify_result(input=open_count[0]['total'], output=1)
        
        tranporter_access_token=brand.tranporter_login()
        cts_indent_count=brand.get_indent_count(tranporter_access_token)
        system.verify_result(input=len(cts_indent_count), output=1)
        
        open_count = filter(lambda active: active['status'] == 'Inprogress', cts_indent_count)
        system.verify_result(input=len(open_count), output=0)

    def test_get_container_lr(self):
        '''
           Test the GET container LR data based on logged in user
           1. Admin sees all the LRs
           2. Transporters see only LRs under him
        '''
        brand = self.brand
        system = self.system
        admin_access_token=self.access_token
        
        saved_cts_indent_data=brand.get_container_lr(admin_access_token)
        system.verify_result(input=len(saved_cts_indent_data), output=4)
        
        tranporter_access_token=brand.tranporter_login()
        saved_cts_indent_data=brand.get_container_lr(tranporter_access_token)
        system.verify_result(input=len(saved_cts_indent_data), output=3)

    def test_save_lr_status(self):
        '''
           Test to change status of an indent to Inprogress and
           update modified date, seal number and container number
           Condition tested: 
           1:If there is any LR Open the indent is Open
           2:If no LR is Open and the current LR is Inprogress
             Indent moves to Inprogress
           3: If all LRs are closed, Indent moves to Closed
        '''
        brand = self.brand
        system = self.system
        admin_access_token=self.access_token
        
        '''Out of 3 LRs LR1 is Open, 
           LR2 is Inporgress and LR3 is Closed
           Thus Indent is Open'''
        saved_cts_indent_data=brand.get_container_indent(admin_access_token)
        system.verify_result(input=saved_cts_indent_data[0]['status'], output='Open')
        saved_cts_lr_data=brand.get_container_lr(admin_access_token)
        system.verify_result(input=saved_cts_lr_data[0]['status'], output='Open')
        
        '''Moving LR1 to Inprogress
           makes LR1 and LR2 Inprogress
           and LR3 Closed. Thus indent is Inprogress'''
        transaction_id=saved_cts_lr_data[0]['transaction_id']
        brand.save_container_lr(admin_access_token, str(transaction_id), 'Inprogress')
        
        saved_cts_indent_data=brand.get_container_indent(admin_access_token)
        system.verify_result(input=saved_cts_indent_data[0]['status'], output='Inprogress')
        saved_cts_lr_data=brand.get_container_lr(admin_access_token)
        system.verify_result(input=saved_cts_lr_data[0]['status'], output='Inprogress')
        
        '''Moving LR1 and LR2 to Closed
           makes all 3 LR as Closed.
           Thus indent is Closed'''
        brand.save_container_lr(admin_access_token, str(saved_cts_lr_data[0]['transaction_id']), 'Closed')
        saved_cts_indent_data=brand.get_container_indent(admin_access_token)
        system.verify_result(input=saved_cts_indent_data[0]['status'], output='Inprogress')
        
        brand.save_container_lr(admin_access_token, str(saved_cts_lr_data[1]['transaction_id']), 'Closed')
        saved_cts_indent_data=brand.get_container_indent(admin_access_token)
        system.verify_result(input=saved_cts_indent_data[0]['status'], output='Closed')
