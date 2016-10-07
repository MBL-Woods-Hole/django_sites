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

    def __str__(self):
        return self.contact


class Dataset(models.Model):
    dataset_id = models.SmallIntegerField(primary_key=True)
    dataset = models.CharField(unique=True, max_length=64)
    dataset_description = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'dataset'

    def __str__(self):
        return self.dataset


class DnaRegion(models.Model):
    dna_region_id = models.AutoField(primary_key=True)
    dna_region    = models.CharField(unique=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'dna_region'

    def __str__(self):
        return self.dna_region

class EnvSampleSource(models.Model):
    env_sample_source_id = models.IntegerField(primary_key=True)
    env_source_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'env_sample_source'

    def __str__(self):
        return "%s: %s" % (self.env_sample_source_id, self.env_source_name)


class IlluminaAdaptor(models.Model):
    illumina_adaptor_id = models.SmallIntegerField(primary_key=True)
    illumina_adaptor = models.CharField(unique=True, max_length=3)

    class Meta:
        managed = False
        db_table = 'illumina_adaptor'
        
    def __unicode__(self):
        return u'{0}'.format(self.illumina_adaptor)        

class IlluminaAdaptorRef(models.Model):
    illumina_adaptor = models.ForeignKey(IlluminaAdaptor, models.DO_NOTHING)
    illumina_index = models.ForeignKey('IlluminaIndex', models.DO_NOTHING)
    illumina_run_key = models.ForeignKey('IlluminaRunKey', models.DO_NOTHING)
    dna_region = models.ForeignKey(DnaRegion, models.DO_NOTHING)
    domain = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'illumina_adaptor_ref'
        unique_together = (('illumina_adaptor', 'dna_region', 'domain'),)


class IlluminaIndex(models.Model):
    illumina_index_id = models.AutoField(primary_key=True)
    illumina_index = models.CharField(unique=True, max_length=6)

    class Meta:
        managed = False
        db_table = 'illumina_index'


class IlluminaRunKey(models.Model):
    illumina_run_key_id = models.AutoField(primary_key=True)
    illumina_run_key = models.CharField(unique=True, max_length=5)

    class Meta:
        managed = False
        db_table = 'illumina_run_key'


class Primer(models.Model):
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


class PrimerSuite(models.Model):
    primer_suite_id = models.SmallIntegerField(primary_key=True)
    primer_suite = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'primer_suite'

    def __str__(self):
        return self.primer_suite

class Project(models.Model):
    project_id = models.SmallIntegerField(primary_key=True)
    project = models.CharField(unique=True, max_length=32)
    title = models.CharField(max_length=64)
    project_description = models.CharField(max_length=255)
    rev_project_name = models.CharField(unique=True, max_length=32)
    funding = models.CharField(max_length=64)
    env_sample_source = models.ForeignKey(EnvSampleSource, models.DO_NOTHING)
    contact = models.ForeignKey(Contact, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'project'

    def label_from_instance(self, obj):
        return "%s" % obj.project

    def __unicode__(self):
        return u'{0}'.format(self.project)        


class RefPrimerSuitePrimer(models.Model):
    primer_suite = models.ForeignKey(PrimerSuite, models.DO_NOTHING)
    primer = models.ForeignKey(Primer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ref_primer_suite_primer'


class Run(models.Model):
    run_id = models.SmallIntegerField(primary_key=True)
    run = models.CharField(max_length=16)
    run_prefix = models.CharField(max_length=7)
    date_trimmed = models.DateTimeField()
    platform = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'run'
        unique_together = (('run', 'platform'),)

    def __str__(self):
        return self.run

class RunInfoIll(models.Model):
    run_info_ill_id = models.AutoField(primary_key=True)
    run_key = models.ForeignKey('RunKey', models.DO_NOTHING)
    run = models.ForeignKey(Run, models.DO_NOTHING)
    lane = models.IntegerField()
    dataset = models.ForeignKey(Dataset, models.DO_NOTHING)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    tubelabel = models.CharField(max_length=32)
    barcode = models.CharField(max_length=4)
    adaptor = models.CharField(max_length=3)
    dna_region = models.ForeignKey(DnaRegion, models.DO_NOTHING)
    amp_operator = models.CharField(max_length=5)
    seq_operator = models.CharField(max_length=5)
    barcode_index = models.CharField(max_length=12)
    overlap = models.CharField(max_length=8)
    insert_size = models.SmallIntegerField()
    file_prefix = models.CharField(max_length=45)
    read_length = models.SmallIntegerField()
    primer_suite = models.ForeignKey(PrimerSuite, models.DO_NOTHING)
    updated = models.DateTimeField()
    platform = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'run_info_ill'
        unique_together = (('run', 'run_key', 'barcode_index', 'lane'),)

    def __str__(self):
        return """run_info_ill_id: %s;
run_key: %s;
run: %s;
lane: %s;
dataset: %s;
project: %s;
tubelabel: %s;
barcode: %s;
adaptor: %s;
dna_region: %s;
amp_operator: %s;
seq_operator: %s;
barcode_index: %s;
overlap: %s;
insert_size: %s;
file_prefix: %s;
read_length: %s;
primer_suite: %s; """ %  (self.run_info_ill_id, self.run_key, self.run, self.lane, self.dataset, self.project, self.tubelabel, self.barcode, self.adaptor, self.dna_region, self.amp_operator, self.seq_operator, self.barcode_index, self.overlap, self.insert_size, self.file_prefix, self.read_length, self.primer_suite)



class RunKey(models.Model):
    run_key_id = models.SmallIntegerField(primary_key=True)
    run_key = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'run_key'
