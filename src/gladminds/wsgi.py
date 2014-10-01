"""
WSGI config for djprotemplate project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import newrelic.agent
PROJECT_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
sys.path.append(PROJECT_DIR)


# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "djprotemplate.settings"

#Change the app_name.settings to your app_name, for example lithium.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gladminds.settings")

NEW_RELIC = os.environ.get('NEW_RELIC', 'newrelic_prod.ini')
from django.conf import settings
NEW_RELIC_FILE = settings.NEW_RELIC_FILE_LOCATION + NEW_RELIC
newrelic.agent.initialize(settings.NEW_RELIC_FILE)

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
application = newrelic.agent.WSGIApplicationWrapper(application)
# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
