import logging
from suds.client import Client
from suds.transport.http import HttpAuthenticated
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from gladminds.bajaj import models
from gladminds.core.auth_helper import Roles
logger = logging.getLogger("gladminds")

class BaseExportFeed(object):

    def __init__(self, username=None, password=None, wsdl_url=None,\
                                                        feed_type=None, feed_remark=None):
        self.username = username
        self.password = password
        self.wsdl_url = wsdl_url
        self.feed_type = feed_type
        self.feed_remark = feed_remark

    def get_http_authenticated(self):
        return HttpAuthenticated(username=self.username,\
                                 password=self.password)

    def get_client(self):
        transport = HttpAuthenticated(\
            username=self.username, password=self.password)
        client = Client(url=self.wsdl_url, transport=transport)
        cache = client.options.cache
        cache.setduration(seconds=settings.FILE_CACHE_DURATION)
        return client

class BaseFeed(object):

    def __init__(self, data_source=None, feed_remark=None):
        self.data_source = data_source
        self.feed_remark = feed_remark

    def import_data(self):
        pass

    def register_user(self, group, username=None, phone_number=None,
                      first_name='', last_name='', email='', address='',
                      state='', pincode=''):
        logger.info('New {0} Registration with id - {1}'.format(group, username))
        try:
            user_group = Group.objects.get(name=group)
        except ObjectDoesNotExist as ex:
            logger.info(
                "[Exception: new_ registration]: {0}"
                .format(ex))
            user_group = Group.objects.create(name=group)
            user_group.save()
        if username:
            try:
                user_details = models.UserProfile.objects.select_related('user').get(user__username=username)
            except ObjectDoesNotExist as ex:
                logger.info(
                    "[Exception: new_ registration]: {0}"
                    .format(ex))    
                new_user = User(
                    username=username, first_name=first_name, last_name=last_name, email=email)
                if group =='customer':
                    password = settings.PASSWORD_POSTFIX
                else:
                    password = username + settings.PASSWORD_POSTFIX
                new_user.set_password(password)
                new_user.save()
                new_user.groups.add(user_group)
                new_user.save()
                logger.info(group + ' {0} registered successfully'.format(username))
                user_details = models.UserProfile(user=new_user,
                                        phone_number=phone_number, address=address,
                                        state=state, pincode=pincode)
                user_details.save()
            return user_details
        else:
            logger.info('{0} id is not provided.'.format(group))
            raise Exception('{0} id is not provided.'.format(group))   

    def check_or_create_dealer(self, dealer_id, address=None, cdms_flag=0):
        try:
            dealer_data = models.Dealer.objects.select_related('user__user').get(
                dealer_id=dealer_id)
            dealer_data.use_cdms = cdms_flag
            dealer_data.save()
        except ObjectDoesNotExist as odne:
            logger.debug(
                "[Exception: new_dealer_data]: {0}"
                .format(odne))
            user = self.register_user(Roles.DEALERS, username=dealer_id)
            dealer_data = models.Dealer(user=user,
                dealer_id=dealer_id, use_cdms=cdms_flag)
            dealer_data.save()            
        return dealer_data

