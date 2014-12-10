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

client  =  Client(SERVER_NAME='bajaj')

class CoreResourceTestCase(ResourceTestCase):
    multi_db=True

    def setUp(self):
        super(CoreResourceTestCase, self).setUp()
