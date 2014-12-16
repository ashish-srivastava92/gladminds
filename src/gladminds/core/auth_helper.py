'''
this file contains all auth related code include group logic , etc
'''
from django.contrib.auth.models import Group, User
from django.conf import settings

ALL_APPS = settings.BRANDS + [settings.GM_BRAND]

class GmApps():
    AFTERBUY = 'afterbuy'
    BAJAJ = 'bajaj'
    DEMO = 'demo'
    GM = 'default'


class Roles():
    SUPERADMINS = 'SuperAdmins'
    ADMINS = 'Admins'
    USERS = 'Users'
    CXOADMINS = 'CxoAdmins'
    FSCSUPERADMINS = 'FscSuperAdmins'
    SDSUPERADMINS = 'SdSuperAdmins'
    FSCSADMINS = 'FscAdmins'
    SDADMINS = 'SdAdmins'

AFTERBUY_ADMIN_GROUPS = [Roles.SUPERADMINS, Roles.ADMINS]
AFTERBUY_GROUPS = [Roles.SUPERADMINS, Roles.ADMINS, Roles.USERS]
OTHER_GROUPS = [Roles.SUPERADMINS, Roles.CXOADMINS, Roles.FSCSUPERADMINS,
                Roles.SDSUPERADMINS, Roles.FSCSADMINS, Roles.SDADMINS]

AFTERBUY_USER_MODELS = ['User', 'Consumer', 'UserProduct', 'ProductSupport', 'RegistrationCertificate',
                        'ProductInsuranceInfo', 'ProductWarrantyInfo', 'PollutionCertificate',
                        'License', 'Invoice', 'SellInformation', 'UserProductImages', 'UserPreference',
                        'UserNotification','Service']


def add_user_to_group(app, user_id, group_name):
    g = Group.objects.using(app).get(name=group_name)
    user = User.objects.using(app).get(id=user_id)
    if not user.groups.using(app).filter(name=group_name).exists():
        user.groups.add(g)
        user.save(using=app)
