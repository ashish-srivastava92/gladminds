from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from django.conf import settings

_AFTERBUY_GROUPS = ['SUPERADMINS', 'ADMINS', 'USERS']
_SERVICE_GROUPS = ['FSCADMINS', 'SDADMINS']
_CXO_GROUPS = ['CXOADMINS']

_ALL_APPS = settings.BRANDS + [settings.GM_BRAND]

_DATABASES = {'gm':settings.ADMIN_DETAILS['gladminds'].get('datbase')}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for group in _AFTERBUY_GROUPS:
            self.add_group('afterbuy', group)

        for app in ['bajaj', 'demo', 'gladminds']:
            for group in _CXO_GROUPS:
                self.add_group(app, group)
            for group in _SERVICE_GROUPS:
                self.add_group(app, group)

        for app in _ALL_APPS:
            ignore_list = []
            for ap in _ALL_APPS:
                if app != ap:
                    ignore_list.append(ap)
            Permission.objects.filter(content_type__app_label__in=ignore_list).using(_DATABASES.get(app, app)).delete()

    def add_group(self, app, group):
        group_count = Group.objects.filter(name=group).using(settings.ADMIN_DETAILS[app].get('database', app)).count()
        if group_count == 0:
            group_obj = Group(name=group)
            group_obj.save(using=settings.ADMIN_DETAILS[app].get('database', app))