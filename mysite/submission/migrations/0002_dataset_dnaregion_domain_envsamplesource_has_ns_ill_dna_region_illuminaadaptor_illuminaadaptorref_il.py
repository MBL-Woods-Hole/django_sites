# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-01 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('dataset_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('dataset', models.CharField(max_length=64, unique=True)),
                ('dataset_description', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'dataset',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DnaRegion',
            fields=[
                ('dna_region_id', models.AutoField(primary_key=True, serialize=False)),
                ('dna_region', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'db_table': 'dna_region',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EnvSampleSource',
            fields=[
                ('env_sample_source_id', models.IntegerField(primary_key=True, serialize=False)),
                ('env_source_name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'env_sample_source',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IlluminaAdaptor',
            fields=[
                ('illumina_adaptor_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('illumina_adaptor', models.CharField(max_length=3, unique=True)),
            ],
            options={
                'db_table': 'illumina_adaptor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IlluminaAdaptorRef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(blank=True, max_length=9, null=True)),
            ],
            options={
                'db_table': 'illumina_adaptor_ref',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IlluminaIndex',
            fields=[
                ('illumina_index_id', models.AutoField(primary_key=True, serialize=False)),
                ('illumina_index', models.CharField(max_length=6, unique=True)),
            ],
            options={
                'db_table': 'illumina_index',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IlluminaRunKey',
            fields=[
                ('illumina_run_key_id', models.AutoField(primary_key=True, serialize=False)),
                ('illumina_run_key', models.CharField(max_length=5, unique=True)),
            ],
            options={
                'db_table': 'illumina_run_key',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Primer',
            fields=[
                ('primer_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('primer', models.CharField(max_length=16, unique=True)),
                ('direction', models.CharField(max_length=1)),
                ('sequence', models.CharField(max_length=64)),
                ('region', models.CharField(max_length=16)),
                ('original_seq', models.CharField(max_length=64)),
                ('domain', models.CharField(blank=True, max_length=9, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'primer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PrimerSuite',
            fields=[
                ('primer_suite_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('primer_suite', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'db_table': 'primer_suite',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('project', models.CharField(max_length=32, unique=True)),
                ('title', models.CharField(max_length=64)),
                ('project_description', models.CharField(max_length=255)),
                ('rev_project_name', models.CharField(max_length=32, unique=True)),
                ('funding', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RefPrimerSuitePrimer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'ref_primer_suite_primer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('run_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('run', models.CharField(max_length=16)),
                ('run_prefix', models.CharField(max_length=7)),
                ('date_trimmed', models.DateTimeField()),
                ('platform', models.CharField(blank=True, max_length=7, null=True)),
            ],
            options={
                'db_table': 'run',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RunInfoIll',
            fields=[
                ('run_info_ill_id', models.AutoField(primary_key=True, serialize=False)),
                ('lane', models.IntegerField()),
                ('tubelabel', models.CharField(max_length=32)),
                ('barcode', models.CharField(max_length=4)),
                ('adaptor', models.CharField(max_length=3)),
                ('amp_operator', models.CharField(max_length=5)),
                ('seq_operator', models.CharField(max_length=5)),
                ('barcode_index', models.CharField(max_length=12)),
                ('overlap', models.CharField(max_length=8)),
                ('insert_size', models.SmallIntegerField()),
                ('file_prefix', models.CharField(max_length=45)),
                ('read_length', models.SmallIntegerField()),
                ('updated', models.DateTimeField()),
                ('platform', models.CharField(blank=True, max_length=7, null=True)),
            ],
            options={
                'db_table': 'run_info_ill',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RunKey',
            fields=[
                ('run_key_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('run_key', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'db_table': 'run_key',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Has_ns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Ill_dna_region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Overlap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]