import csv
import logging
import os
import time
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.db.models import signals

from gladminds.bajaj.services import message_template as templates
from gladminds.core import utils
from gladminds.bajaj import models
from gladminds.core.managers.audit_manager import feed_log, sms_log
from gladminds.core.cron_jobs.queue_utils import send_job_to_queue

logger = logging.getLogger("gladminds")
USER_GROUP = {'dealer': 'dealers', 'ASC': 'ascs', 'SA':'sas', 'customer':"customer"}

class LoyaltyFeed(object):

    def import_to_db(self, feed_type=None, data_source=[], feed_remark=None):
        function_mapping = {
            'part_master': PartMasterFeed,
            'part_upc': PartUPCFeed,
            'part_point': PartPointFeed,
#             'distributor': DistributorFeed,
#             'mechanic': MechanicFeed
        }
        feed_obj = function_mapping[feed_type](data_source=data_source,
                                             feed_remark=feed_remark)
        return feed_obj.import_data()

class BaseFeed(object):

    def __init__(self, data_source=None, feed_remark=None):
        self.data_source = data_source
        self.feed_remark = feed_remark


class PartMasterFeed(BaseFeed):

    def import_data(self):
        total_failed = 0
        for spare in self.data_source:
            try:
                part_data = models.SparePartMasterData.objects.get(part_number=spare['part_number'])
            except ObjectDoesNotExist as done:
                logger.info(
                    '[Info: PartMasterFeed_part_data]: {0}'.format(done))
                try:
                    spare_type_object = models.ProductType.objects.filter(product_type=spare['part_type'])
                    if not spare_type_object:
                        spare_type_object = models.ProductType(product_type=spare['part_type'])
                        spare_type_object.save()
                    else:
                        spare_type_object = spare_type_object[0]
                    spare_object = models.SparePartMasterData(
                                                product_type=spare_type_object,
                                                part_number = spare['part_number'],
                                                part_model = spare['part_model'],
                                                description = spare['description'],
                                                category = spare['category'],
                                                segment_type = spare['segment'],
                                                supplier = spare['supplier']
                                    )
                    spare_object.save()
                except Exception as ex:
                    total_failed += 1
                    ex = "{0}".format(ex)
                    logger.error(ex)
                    self.feed_remark.fail_remarks(ex)
                    continue
        return self.feed_remark


class PartUPCFeed(BaseFeed):

    def import_data(self):
        total_failed = 0
        for spare in self.data_source:
            try:
                part_data = models.SparePartMasterData.objects.get(part_number=spare['part_number'])
                spare_object = models.SparePartUPC(
                                            part_number=part_data,
                                            unique_part_code = spare['UPC'])
                spare_object.save()
            except Exception as ex:
                total_failed += 1
                ex = "[PartUPCFeed]: part-{0} , UPC-{1} :: {2}".format(spare['part_number'],
                                                            spare['UPC'], ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
                continue

        return self.feed_remark

class PartPointFeed(BaseFeed):

    def import_data(self):
        total_failed = 0
        for spare in self.data_source:
            try:
                part_data = models.SparePartMasterData.objects.get(part_number=spare['part_number'])
                spare_object = models.SparePartPoint.objects.filter(part_number=part_data,
                                                     territory=spare['territory'])
                if not spare_object:
                    spare_object = models.SparePartPoint(part_number = part_data,
                                              points = spare['points'],
                                              price = spare['price'],
                                              MRP = spare['mrp'],
                                              valid_from = spare['valid_from'],
                                              valid_till = spare['valid_to'],
                                              territory = spare['territory'])
                    spare_object.save()
                else:
                    raise ValueError('Points of the part already exists for the territory: ' + spare['territory'])
            except Exception as ex:
                total_failed += 1
                ex = "[PartPointFeed]: part-{0} :: {1}".format(spare['part_number'], ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
                continue

        return self.feed_remark
