from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.conf import settings

from gladminds.admin import admin

_DEMO = 'demo'
_BAJAJ = 'bajaj'
_AFTERBUY = 'afterbuy'
_GM = 'gladminds'


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('syncdb', database=_DEMO, interactive=False)
        call_command('syncdb', database=_BAJAJ, interactive=False)
        call_command('syncdb', database=_AFTERBUY, interactive=False)
        call_command('syncdb', interactive=False)
        self.create_admin(_DEMO)
        self.create_admin(_BAJAJ)
        self.create_admin(_AFTERBUY)
        self.create_admin(_GM)

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
