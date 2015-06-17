from django.core.management.base import BaseCommand
from django.core.management import call_command

_DEMO = 'demo'
_BAJAJ = 'bajaj'
_AFTERBUY = 'afterbuy'
_GM = 'gm'

_COMMAND = 'schemamigration'

class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command(_COMMAND, _BAJAJ, auto=True)
        call_command(_COMMAND, _DEMO, auto=True)
        call_command(_COMMAND, _AFTERBUY, auto=True)
        call_command(_COMMAND, _GM, auto=True)