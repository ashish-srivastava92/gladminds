from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User, Permission, Group
from django.conf import settings
from gladminds.afterbuy.models import Consumer
from gladminds.core.auth_helper import AFTERBUY_GROUPS, add_user_to_group,\
    OTHER_GROUPS, Roles, GmApps

_DEMO = GmApps.DEMO
_BAJAJ = GmApps.BAJAJ
_AFTERBUY = GmApps.AFTERBUY
_GM = 'gladminds'


_ALL_APPS = settings.BRANDS + [settings.GM_BRAND]

_DATABASES = {'gm':settings.ADMIN_DETAILS['gladminds'].get('database')}

_AFTERBUY_ADMINS = [{'email':'karthik.rajagopalan@gladminds.co', 'username': 'karthik.rajagopalan', 'phone':'9741200991'},
                    {'email':'praveen.m@gladminds.co', 'username':'praveen.m', 'phone':'8867576306'}
                    ]

_AFTERBUY_SUPERADMINS = [{'email':'naveen.shankar@gladminds.co', 'username':'naveen.shankar', 'phone':'9880747576'},
                         {'email':'afterbuy@gladminds.co', 'username':'afterbuy', 'phone':'9999999999'}
                    ]

class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('syncdb', database=_DEMO, interactive=False)
        call_command('syncdb', database=_BAJAJ, interactive=False)
        call_command('syncdb', database=_AFTERBUY, interactive=False)
        call_command('syncdb', interactive=False)
        self.define_groups()
        self.create_admin(_DEMO)
        self.create_admin(_BAJAJ)
        self.create_admin(_GM)
        self.create_afterbuy_admins()
        #self.set_permissions()

    def set_permissions(self):
        try:
            for app in _ALL_APPS:
                add_user_to_group(app, 1, Roles.SUPERADMINS)
            if not Consumer.objects.filter(user=1).exists():
                Consumer(user__id=1, phone_number=9999999999).save()
        except:
            pass

    def define_groups(self):
        for group in AFTERBUY_GROUPS:
            self.add_group(GmApps.AFTERBUY, group)

        for app in [GmApps.BAJAJ, GmApps.DEMO, 'gladminds']:
            for group in OTHER_GROUPS:
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

    def create_afterbuy_admins(self):
        for details in _AFTERBUY_ADMINS:
            self.create_consumer(details, Roles.ADMINS)
        for details in _AFTERBUY_SUPERADMINS:
            self.create_consumer(details, Roles.SUPERADMINS)

    def create_consumer(self, details, group):
        app = GmApps.AFTERBUY
        username = details['username']
        phone = details['phone']
        email = details['email']
        password = settings.ADMIN_DETAILS[app]['password']
        database = settings.ADMIN_DETAILS[app].get('database', app)

        user = User.objects.filter(username=username).using(database).count()
        if user == 0:
            admin = User.objects.using(database).create(username=username)
            admin.set_password(password)
            admin.is_superuser = True
            admin.is_staff = True
            admin.email = email
            admin.save(using=database)
            Consumer(user=admin, phone_number=phone, is_email_verified=True).save()
            add_user_to_group(app, admin.id, group)