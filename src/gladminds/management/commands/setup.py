from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User, Permission, Group
from django.conf import settings
from gladminds.core.utils import add_user_to_group
from gladminds.afterbuy.models import Consumer

_DEMO = 'demo'
_BAJAJ = 'bajaj'
_AFTERBUY = 'afterbuy'
_GM = 'gladminds'

_AFTERBUY_GROUPS = ['SuperAdmins', 'Admins', 'Users']
_OTHER_GROUPS = ['SuperAdmins', 'CxoAdmins', 'FscSuperAdmins', 'SdSuperAdmins', 'FscAdmins', 'SdAdmins']

_ALL_APPS = settings.BRANDS + [settings.GM_BRAND]

_DATABASES = {'gm':settings.ADMIN_DETAILS['gladminds'].get('database')}

class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('syncdb', database=_DEMO, interactive=False)
        call_command('syncdb', database=_BAJAJ, interactive=False)
        call_command('syncdb', database=_AFTERBUY, interactive=False)
        call_command('syncdb', interactive=False)
        self.define_groups()
        self.create_admin(_DEMO)
        self.create_admin(_BAJAJ)
        self.create_admin(_AFTERBUY)
        self.create_admin(_GM)
        #self.set_permissions()

    def set_permissions(self):
        try:
            for app in _ALL_APPS:
                add_user_to_group(app, 1, 'SUPERADMINS')
            if not Consumer.objects.filter(user=1).exists():
                Consumer(user__id=1, phone_number=9999999999).save()
        except:
            pass

    def define_groups(self):
        for group in _AFTERBUY_GROUPS:
            self.add_group('afterbuy', group)

        for app in ['bajaj', 'demo', 'gladminds']:
            for group in _OTHER_GROUPS:
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

    def create_admin(self, app):
        name = settings.ADMIN_DETAILS[app]['user']
        password = settings.ADMIN_DETAILS[app]['password']
        database = settings.ADMIN_DETAILS[app].get('database', app)

        user = User.objects.filter(username=name).using(database).count()
        if user == 0:
            admin = User.objects.using(database).create(username=name)
            admin.set_password(password)
            admin.is_superuser = True
            admin.is_staff = True
            admin.save(using=database)
