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
