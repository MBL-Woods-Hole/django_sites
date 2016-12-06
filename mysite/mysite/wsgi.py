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
import logging

logging.basicConfig(filename='/usr/local/www/vamps/tmp/django_submission.log', level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')



path = '/usr/local/www/vampsdev/projects/django/illumina_submission/django_sites/mysite/mysite'
# sys.path.append('<PATH_TO_MY_DJANGO_PROJECT>/hellodjango')
# 
# add the virtualenv site-packages path to the sys.path
sys.path.append('/bioware/python-2.7.11-201608021657/lib/python2.7/site-packages/Django-1.10-py2.7.egg/django')
# 
# # poiting to the project settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hellodjango.settings")


if path not in sys.path:
    sys.path.append(path)

logging.info('"path = ')
logging.info(path)
logging.info('sys.path = ')
logging.info(sys.path)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

