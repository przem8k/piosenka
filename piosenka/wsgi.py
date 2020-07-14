"""
WSGI config for testpzt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "piosenka.settings"
os.environ["LANG"] = "pl_PL.UTF-8"
os.environ["LC_ALL"] = "pl_PL.UTF-8"
os.environ["LC_LANG"] = "pl_PL.UTF-8"

application = get_wsgi_application()
