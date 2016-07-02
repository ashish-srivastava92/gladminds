from django import template
from django.contrib.auth.models import User
import json
from django.conf import settings

register = template.Library()
ROLES_MAP = {  'Distributors': 1,
               'SFAAdmins': 2,
               'AreaSparesManagers': 3,
               'NationalSparesManagers': 4,
               'SuperAdmins': 100
            }

@register.filter(name='rbac')
def fetch_user_for_rbac(arg):
    user = User.objects.get(username=arg)
    for group in user.groups.all():
    	return ROLES_MAP[group.name]
    return 300

@register.filter(name='verticle')
def fetch_verticle(arg):
	return str(settings.BRAND_VERTICLE)
