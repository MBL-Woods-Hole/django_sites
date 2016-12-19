"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
import logging
logging.basicConfig(filename='/usr/local/www/vamps/tmp/django_submission.log', 
                    format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG)

mysite_path = '/usr/local/www/vampsdev/projects/django/illumina_submission/django_sites/'
mysite_path1 = '/usr/local/www/vampsdev/projects/django/illumina_submission/django_sites/mysite'


if mysite_path not in sys.path:
    sys.path.append(mysite_path)
if mysite_path1 not in sys.path:
    sys.path.append(mysite_path1)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

try:
    activate_this = '/usr/local/www/vamps/server/illumina-submission/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
except IOError:
    pass
except:
    raise

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

