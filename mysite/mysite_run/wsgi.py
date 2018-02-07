"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
# import stat
import sys
import logging
log_filename = '/usr/local/www/vamps/tmp/django_submission.log'
logging.basicConfig(filename=log_filename, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG)

# st = os.stat(log_filename)
# logging.debug("st.st_mode")
# logging.debug(st.st_mode)
# 
# os.chmod(log_filename, st.st_mode | stat.S_IWGRP)

# os.chmod(log_filename, stat.S_IRWXU | stat.S_IRUSR | stat.S_IWGRP)
# os.chmod(log_filename,  stat.S_IWGRP)
                    

mysite_path = '/usr/local/www/vampsdev/projects/django/illumina_submission/django_sites/'
mysite_path1 = '/usr/local/www/vampsdev/projects/django/illumina_submission/django_sites/mysite'
mysite_path2 = '/usr/local/www/vampsdev/projects/django/illumina_submission/django_sites/mysite/mysite_run'


if mysite_path not in sys.path:
    sys.path.append(mysite_path)
if mysite_path1 not in sys.path:
    sys.path.append(mysite_path1)
if mysite_path2 not in sys.path:
    sys.path.append(mysite_path2)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite_run.settings")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

try:
    activate_this = '/usr/local/www/vamps/server/illumina-submission/bin/activate_this.py'
    try:
        execfile(activate_this, dict(__file__=activate_this))
    except:
        # execfile(filename, globals, locals)
        # by
        exec (compile(open(activate_this, "rb").read(), activate_this, 'exec'), dict(__file__=activate_this))
except IOError:
    pass
except:
    raise

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

