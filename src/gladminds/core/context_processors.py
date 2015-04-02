from django.conf import settings
from django.contrib.sites.models import Site
from gladminds.core.auth_helper import Roles
from gladminds.settings import S3_BASE_URL
from gladminds.core import utils

def current_site(request):
    return (settings.SITE_ID) and {'site': Site.objects.get_current()} or {}

def gm_constants(request):
    '''
    Contains all the constants used in Service Desk ex : SDO, SDM
    '''
    constants = {'SD_CONSTANTS':{}}
    constants['SD_CONSTANTS'] = {'SD_MANAGER' : Roles.SDMANAGERS, 
            'SD_OWNER' : Roles.SDOWNERS, 
            'DEALER' : Roles.DEALERS,
            'ASC': Roles.ASCS,
            'SD_READONLY': Roles.SDREADONLY,
            'FSCADMIN':Roles.FSCADMINS}
    brand_meta = settings.BRAND_META.get(settings.BRAND, {})
    user_groups = utils.get_user_groups(request.user)
    brand_url = settings.HOME_URLS.get(settings.BRAND, {})
    brand_services = []
    
    for user_group in user_groups:
        if user_group in brand_url.keys():
            values = brand_url[user_group]
            for value in values:
                services = {} 
                services['url'] = value.values()[0]
                services['name'] = value.keys()[0]
                brand_services.append(services)
    
    return { 'CONSTANTS' :constants, 'S3_URL' : S3_BASE_URL,
            'METAINFO': brand_meta, 'METAURL': brand_services, 
            'BRAND': settings.BRAND }

