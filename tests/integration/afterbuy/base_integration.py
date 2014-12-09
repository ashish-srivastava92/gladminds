import os
import json

from django.conf import settings
from django.test.client import Client
from tastypie.test import ResourceTestCase
from django.core import management
from django.contrib.auth.models import User
from gladminds.bajaj import models as common
from gladminds.management.commands import load_gm_migration_data
from gladminds.bajaj import models as aftersell_common
from integration.core.base_integration import CoreResourceTestCase

client  =  Client(SERVER_NAME='bajaj')

class AfterBuyResourceTestCase(CoreResourceTestCase):

    def setUp(self):
        super(AfterBuyResourceTestCase, self).setUp()
        load_email_obj = load_gm_migration_data.Command()
        load_email_obj.add_email_template()
        load_email_obj.add_sms_template()
        load_email_obj.add_group()
        self.MESSAGE_URL = "/v1/messages"
