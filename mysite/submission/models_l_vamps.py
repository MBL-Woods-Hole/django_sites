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

class VampsSubmissions(models.Model):
    submit_code = models.CharField(unique=True, max_length=40)
    user_id = models.IntegerField()
        # models.ForeignKey(User, models.DO_NOTHING)
    temp_project = models.CharField(max_length=100)
    title = models.CharField(max_length=132)
    project_description = models.CharField(max_length=255)
    funding = models.CharField(max_length=64)
    num_of_tubes = models.SmallIntegerField()
    date_initial = models.DateField()
    date_updated = models.DateField()
    locked = models.IntegerField(blank=True, null=True)

    class Meta:
        vamps_db = True
        managed = False
        db_table = 'vamps_submissions'

    def __str__(self):
        return "%s: %s" % (self.submit_code, self.temp_project)

OVERLAPCHOICE = (
    ('complete', 'complete'),
    ('partial', 'partial'),
    ('none', 'none'),
)

class VampsSubmissionsTubes(models.Model):
    submit_code = models.CharField(max_length=40)
    tube_number = models.IntegerField()
    tube_label = models.CharField(max_length=20)
    dataset_description = models.CharField(max_length=100)
    duplicate = models.CharField(max_length=5)
    domain = models.CharField(max_length=8, blank=True, null=True)
    primer_suite = models.CharField(max_length=60)
    dna_region = models.CharField(max_length=40)
    project_name = models.CharField(max_length=64)
    dataset_name = models.CharField(max_length=64)
    runkey = models.CharField(max_length=25)
    barcode = models.CharField(max_length=10)
    pool = models.CharField(max_length=30)
    lane = models.CharField(max_length=5)
    direction = models.CharField(max_length=5)
    platform = models.CharField(max_length=15)
    op_amp = models.CharField(max_length=5)
    op_seq = models.CharField(max_length=5)
    op_empcr = models.CharField(max_length=5)
    enzyme = models.CharField(max_length=10)
    rundate = models.CharField(max_length=10)
    adaptor = models.CharField(max_length=3)
    date_initial = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    on_vamps = models.CharField(max_length=10)
    sample_received = models.CharField(max_length=15)
    concentration = models.DecimalField(max_digits=10, decimal_places=4)
    quant_method = models.CharField(max_length=15)
    overlap = models.CharField(max_length=8,choices=OVERLAPCHOICE)
    insert_size = models.IntegerField()
    barcode_index = models.CharField(max_length=12, blank=True, null=True)
    read_length = models.SmallIntegerField(blank=True, null=True)
    trim_distal = models.CharField(max_length=5, blank=True, null=True)
    env_sample_source = models.ForeignKey('NewEnvSampleSource', models.DO_NOTHING)
    # env_sample_source = models.ForeignKey(verbose_name='NewEnvSampleSource')

    class Meta:
        vamps_db = True
        managed = False
        db_table = 'vamps_submissions_tubes'
        unique_together = (('submit_code', 'tube_number'),)

    def __str__(self):
        return "%s: %s, %s, %s" % (self.submit_code, self.project_name, self.dataset_name, self.dna_region)

class NewEnvSampleSource(models.Model):
    env_sample_source_id = models.IntegerField(primary_key=True)
    env_source_name = models.CharField(unique=True, max_length=50)

    class Meta:
        vamps_db = True
        db_table = 'new_env_sample_source'

    def __str__(self):
        return "%s: %s" % (self.env_sample_source_id, self.env_source_name)
