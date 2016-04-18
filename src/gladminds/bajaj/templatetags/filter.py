from django import template
from django.contrib.auth.models import User
import json

register = template.Library()


@register.filter(name='rbac')
def fetch_user_for_rbac(arg):
    user = User.objects.get(username=arg)
    for group in user.groups.all():
    	if group.name == 'Distributors':
    		return 1
    	if group.name == 'SFAAdmins':
    		return 2
    	if group.name == 'AreaSparesManagers':
    		return 3
    	if group.name == 'NationalSparesManagers':
    		return 4
    return 300
