from django.conf import settings
from django.contrib.sites.models import Site
from gladminds.core.auth_helper import Roles

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
            'ASC': Roles.ASCS}
    return { 'constants' :constants }

