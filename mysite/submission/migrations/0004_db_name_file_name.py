# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-02-07 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_newenvsamplesource_vampsauth_vampssubmissions_vampssubmissionstubes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Db_name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='File_name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
