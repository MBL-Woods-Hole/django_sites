# -*- coding: utf-8 -*-
# import settings

class submissionRouter(object): 
  
    def db_for_read(self, model, **hints):
      """
      Send reads on a specific model to the appropriate db
      """
      db = 'default'

      """
      This snippet is particular to my own use case - the databases I'm reporting on 
      have tables with unique prefixes, so I'm able to find that prefix in the 
      model._meta.db_table value to determine which database I need to point to.

      But you'll probably need to solve this problem in a different way.  Take a 
      look at this page for some other model._meta attributes you can use:
      https://docs.djangoproject.com/en/dev/ref/models/options/
      """
      import re
      one = re.search('firstartist_', model._meta.db_table)
      two = re.search('secondartist_', model._meta.db_table)
      if g:
        db = 'dbone'
      if p:
        db = 'dbtwo'
      return db
  
    def db_for_read(self, model, **hints):
        """
        From http://www.mechanicalgirl.com/post/reporting-django-multi-db-support/
        Send reads on a specific model to the appropriate db
        """
        db = 'default'

        # if model._meta.app_label.startswith('Env454'):
        #   db = 'local_env454'
        if model._meta.app_label == 'submission':
          print "111"
          print model._meta.db_table
          print "=" *10
          if model._meta.db_table.startswith('vamps_'):
            print "local_vamps 222"
            db = 'local_vamps'
          else:
            print "local_env454 333"
            db = 'local_env454'
      
        # "Point all operations on submission models to 'local_env454'"
        # if model._meta.app_label == 'submission':
        #     return 'local_env454'
        print "db = %s DDDD" % db
        return db

    def db_for_write(self, model, **hints):
        "Point all operations on submission models to 'local_env454'"
        if model._meta.app_label == 'submission':
            return None
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('local_env454', 'test_vamps')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

        # "Allow any relation if a both models in submission app"
        # if obj1._meta.app_label == 'submission' and obj2._meta.app_label == 'submission':
        #     return True
        # # Allow if neither is submission app
        # elif 'submission' not in [obj1._meta.app_label, obj2._meta.app_label]: 
        #     return True
        # return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return False


    def allow_syncdb(self, db, model):
        if db == 'test_vamps' or db == 'local_env454' or model._meta.app_label == "submission":
            return False # we're not using syncdb on our legacy database
        else: # but all other models/databases are fine
            return True

# class DatabaseAppsRouter(object):
# http://diegobz.net/2011/02/10/django-database-router-using-settings/
