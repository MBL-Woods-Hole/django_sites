from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Contact(models.Model):
    contact_id = models.SmallIntegerField(primary_key=True)
    contact = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    institution = models.CharField(max_length=128)
    vamps_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'
        unique_together = (('contact', 'email', 'institution'),)
