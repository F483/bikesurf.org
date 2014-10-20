"""
WSGI config for bikesurf.org project.

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
import site

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# add the site-packages of the virtualenv
site.addsitedir(os.path.join(PROJECT_DIR, 'env/local/lib/python2.7/site-packages'))

# add the app's directory to the PYTHONPATH
sys.path.append(PROJECT_DIR)

# activate virtual env
activate_env=os.path.expanduser(os.path.join(PROJECT_DIR, "env/bin/activate_this.py"))
execfile(activate_env, dict(__file__=activate_env))

# path to settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

