"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

# import os
# 
# from django.core.wsgi import get_wsgi_application
# 
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# 
# application = get_wsgi_application()

import os
import sys

path = '/usr/local/www/vampsdev/projects/django/illumina_submission/django_sites/mysite/mysite'
if path not in sys.path:
    sys.path.append(path)
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
    
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

