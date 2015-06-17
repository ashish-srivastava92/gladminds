from django.core.management.base import BaseCommand
from django.core.management import call_command

from south.management.commands import migrate
_DEMO = 'demo'
_BAJAJ = 'bajaj'
_AFTERBUY = 'afterbuy'
_GM = 'gm'


class Command(BaseCommand):

    def handle(self, *args, **options):
        #call_command('migrate', _BAJAJ, '0001', fake=True)
        call_command('migrate', _BAJAJ)
        #call_command('migrate', _DEMO, '0001', fake=True)
        call_command('migrate', _DEMO)
        #call_command('migrate', _AFTERBUY, '0001', fake=True)
        call_command('migrate', _AFTERBUY)
        call_command('migrate', _GM, '0001', fake=True)
        call_command('migrate', _GM, interactive=False)