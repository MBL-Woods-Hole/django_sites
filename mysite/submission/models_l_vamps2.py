# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class ModelChoiceIterator(object):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    self.choice(obj) for obj in self.queryset.all()
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            try:
                for obj in self.queryset:
                    yield self.choice(obj)
            except TypeError:
                for obj in self.queryset.all():
                    yield self.choice(obj)

class AllMethodCachingQueryset(models.query.QuerySet):
    def all(self, get_from_cache=True):
        if get_from_cache:
            return self
        else:
            return self._clone()

class AllMethodCachingManager(models.Manager):
    def get_query_set(self):
        return AllMethodCachingQueryset(self.model, using=self._db)
models.options.DEFAULT_NAMES = models.options.DEFAULT_NAMES + ('vamps2',)

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(max_length=64)
        # models.CharField(max_length=64)
    institution = models.CharField(max_length=128, blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    active = models.IntegerField()
    security_level = models.IntegerField(blank=True, null=True)
    encrypted_password = models.CharField(max_length=50)
    sign_in_count = models.IntegerField()
    current_sign_in_at = models.TimeField()
    last_sign_in_at = models.TimeField()


    def __str__(self):
        return "%s, %s %s, %s" % (self.user, self.first_name, self.last_name, self.institution)

    class Meta:
        vamps2 = True
        managed = False
        db_table = 'user'
        unique_together = (('first_name', 'last_name', 'email', 'institution'),)

class ProjectVamps2(models.Model):
    objects = models.Manager()
    cache_all_method = AllMethodCachingManager()

    # form_class.base_fields['foo'].queryset = YourModel.cache_all_method.all()
    #   `project_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    #   `project` varchar(32) NOT NULL DEFAULT '',
    #   `title` varchar(255) NOT NULL DEFAULT '',
    #   `project_description` text NOT NULL,
    #   `rev_project_name` varchar(32) NOT NULL DEFAULT '',
    #   `funding` varchar(64) NOT NULL DEFAULT '',
    #   `owner_user_id` int(11) unsigned DEFAULT NULL,
    #   `public` tinyint(1) NOT NULL DEFAULT '0',
    #   `metagenomic` tinyint(1) DEFAULT '0',
    #   `matrix` tinyint(1) DEFAULT '0',
    #   `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
    #   `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
    #   `active` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'if 0 the project is invisible on VAMPS2',
    #   `permanent` tinyint(1) NOT NULL DEFAULT '1',
    #   `user_project` tinyint(1) DEFAULT '0',

    project_id = models.IntegerField(primary_key=True)
    project = models.CharField(unique=True, max_length=32)
    title = models.CharField(max_length=255)
    project_description = models.CharField(max_length=255)
    rev_project_name = models.CharField(unique=True, max_length=32)
    funding = models.CharField(max_length=64)
    # owner_user_id = models.IntegerField()
        # ForeignKey(
        # User,
        # on_delete=models.CASCADE,
        # related_name='user_id',
        # db_column='owner_user_id',
    # )
    public = models.PositiveSmallIntegerField(default=0)
    metagenomic = models.PositiveSmallIntegerField(default=0)
    matrix = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    active = models.PositiveSmallIntegerField(default=0)
    permanent = models.PositiveSmallIntegerField(default=1)
    user_project = models.PositiveSmallIntegerField(default=0)

    class Meta:
        vamps2 = True
        managed = False
        db_table = 'project'

    def __str__(self):
        # pass
        return "%s" % (self.project)