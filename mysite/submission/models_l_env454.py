# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

models.options.DEFAULT_NAMES = models.options.DEFAULT_NAMES + ('env454_db',)


class Env454_Contact(models.Model):
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

    def __str__(self):
        return self.contact


class Env454_Dataset(models.Model):
    dataset_id = models.SmallIntegerField(primary_key=True)
    dataset = models.CharField(unique=True, max_length=64)
    dataset_description = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'dataset'

    def __str__(self):
        return self.dataset


class Env454_DnaRegion(models.Model):
    dna_region_id = models.AutoField(primary_key=True)
    dna_region = models.CharField(unique=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'dna_region'

    def __str__(self):
        return self.dna_region

class Env454_EnvSampleSource(models.Model):
    env_sample_source_id = models.IntegerField(primary_key=True)
    env_source_name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return "%s: %s" % (self.env_sample_source_id, self.env_source_name)


    class Meta:
        managed = False
        db_table = 'env_sample_source'


class Env454_IlluminaAdaptor(models.Model):
    illumina_adaptor_id = models.SmallIntegerField(primary_key=True)
    illumina_adaptor = models.CharField(unique=True, max_length=3)

    class Meta:
        managed = False
        db_table = 'illumina_adaptor'


class Env454_IlluminaAdaptorRef(models.Model):
    illumina_adaptor = models.ForeignKey(Env454_IlluminaAdaptor, models.DO_NOTHING)
    illumina_index = models.ForeignKey('IlluminaIndex', models.DO_NOTHING)
    illumina_run_key = models.ForeignKey('IlluminaRunKey', models.DO_NOTHING)
    dna_region = models.ForeignKey(Env454_DnaRegion, models.DO_NOTHING)
    domain = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'illumina_adaptor_ref'
        unique_together = (('illumina_adaptor', 'dna_region', 'domain'),)


class Env454_IlluminaIndex(models.Model):
    illumina_index_id = models.AutoField(primary_key=True)
    illumina_index = models.CharField(unique=True, max_length=6)

    class Meta:
        managed = False
        db_table = 'illumina_index'


class Env454_IlluminaRunKey(models.Model):
    illumina_run_key_id = models.AutoField(primary_key=True)
    illumina_run_key = models.CharField(unique=True, max_length=5)

    class Meta:
        managed = False
        db_table = 'illumina_run_key'


class Env454_Primer(models.Model):
    primer_id = models.SmallIntegerField(primary_key=True)
    primer = models.CharField(unique=True, max_length=16)
    direction = models.CharField(max_length=1)
    sequence = models.CharField(max_length=64)
    region = models.CharField(max_length=16)
    original_seq = models.CharField(max_length=64)
    domain = models.CharField(max_length=9, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'primer'


class Env454_PrimerSuite(models.Model):
    primer_suite_id = models.SmallIntegerField(primary_key=True)
    primer_suite = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'primer_suite'


class Env454_Project(models.Model):
    project_id = models.SmallIntegerField(primary_key=True)
    project = models.CharField(unique=True, max_length=32)
    title = models.CharField(max_length=64)
    project_description = models.CharField(max_length=255)
    rev_project_name = models.CharField(unique=True, max_length=32)
    funding = models.CharField(max_length=64)
    env_sample_source = models.ForeignKey(Env454_EnvSampleSource, models.DO_NOTHING)
    contact = models.ForeignKey(Env454_Contact, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'project'


class Env454_RefPrimerSuitePrimer(models.Model):
    primer_suite = models.ForeignKey(Env454_PrimerSuite, models.DO_NOTHING)
    primer = models.ForeignKey(Env454_Primer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ref_primer_suite_primer'


class Env454_Run(models.Model):
    run_id = models.SmallIntegerField(primary_key=True)
    run = models.CharField(max_length=16)
    run_prefix = models.CharField(max_length=7)
    date_trimmed = models.DateTimeField()
    platform = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'run'
        unique_together = (('run', 'platform'),)


class Env454_RunInfo(models.Model):
    run_info_id = models.SmallIntegerField(primary_key=True)
    run_key = models.ForeignKey('RunKey', models.DO_NOTHING)
    run = models.ForeignKey(Env454_Run, models.DO_NOTHING)
    lane = models.IntegerField()
    direction = models.CharField(max_length=4, blank=True, null=True)
    dataset = models.ForeignKey(Env454_Dataset, models.DO_NOTHING)
    project = models.ForeignKey(Env454_Project, models.DO_NOTHING)
    tubelabel = models.CharField(max_length=32)
    barcode = models.CharField(max_length=4)
    adaptor = models.CharField(max_length=1, blank=True, null=True)
    pool = models.CharField(max_length=32)
    dna_region = models.ForeignKey(Env454_DnaRegion, models.DO_NOTHING)
    amp_operator = models.CharField(max_length=5)
    seq_operator = models.CharField(max_length=5)
    empcr_operator = models.CharField(max_length=5)
    platform = models.CharField(max_length=11, blank=True, null=True)
    concentration = models.DecimalField(max_digits=10, decimal_places=4)
    quant_method = models.ForeignKey('QuantMethod', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'run_info'
        unique_together = (('run', 'run_key', 'lane', 'direction', 'platform'),)


class Env454_RunInfoIll(models.Model):
    run_info_ill_id = models.AutoField(primary_key=True)
    run_key = models.ForeignKey('RunKey', models.DO_NOTHING)
    run = models.ForeignKey(Env454_Run, models.DO_NOTHING)
    lane = models.IntegerField()
    dataset = models.ForeignKey(Env454_Dataset, models.DO_NOTHING)
    project = models.ForeignKey(Env454_Project, models.DO_NOTHING)
    tubelabel = models.CharField(max_length=32)
    barcode = models.CharField(max_length=4)
    adaptor = models.CharField(max_length=3)
    dna_region = models.ForeignKey(Env454_DnaRegion, models.DO_NOTHING)
    amp_operator = models.CharField(max_length=5)
    seq_operator = models.CharField(max_length=5)
    barcode_index = models.CharField(max_length=12)
    overlap = models.CharField(max_length=8)
    insert_size = models.SmallIntegerField()
    file_prefix = models.CharField(max_length=45)
    read_length = models.SmallIntegerField()
    primer_suite = models.ForeignKey(Env454_PrimerSuite, models.DO_NOTHING)
    updated = models.DateTimeField()
    platform = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'run_info_ill'
        unique_together = (('run', 'run_key', 'barcode_index', 'lane'),)


class Env454_RunKey(models.Model):
    run_key_id = models.SmallIntegerField(primary_key=True)
    run_key = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'run_key'
