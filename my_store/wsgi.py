"""
WSGI config for my_store project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys


# додайте шлях до вашого проекту
path = '/home/venator3/mysite'
if path not in sys.path:
    sys.path.append(path)

# встановіть змінну оточення для вашого проекту
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_store.settings'

# завантажте Django WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import sys

# assuming your Django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/myusername/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

## Uncomment the lines below depending on your Django version
###### then, for Django >=1.5:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
###### or, for older Django <=1.4
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
