# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

models.options.DEFAULT_NAMES = models.options.DEFAULT_NAMES + ('vamps_db',)

class User(models.Model):
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
        vamps_db = True
        managed = False
        db_table = 'user'
        unique_together = (('first_name', 'last_name', 'email', 'institution'),)