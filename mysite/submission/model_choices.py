from django.db import models

class Machine(models.Model):
    # machine_id = models.SmallIntegerField(primary_key=True)
    # machine    = models.CharField(max_length=16)
    # short_name =

    MACHINE_CHOICES = (
        ('ms', 'miseq'),
        ('hs', 'hiseq'),
        ('ns', 'nextseq'),
    )

    MACHINE_SHORTCUTS_CHOICES = (
        ('miseq'  , 'ms'),
        ('hiseq'  , 'hs'),
        ('nextseq', 'ns'),
    )

    PLATFORM_CHOICES = (
        ('miseq', 'MiSeq'),
        ('hiseq', 'HiSeq'),
        ('nextseq', 'NextSeq'),
    )

class Db_name(models.Model):
    DB_NAME_CHOICES = (
        ('env454', 'env454'),
        ('vamps2', 'vamps2'),
    )

class Overlap(models.Model):

    COMPLETE_OVERLAP_CHOICES = (
        ('ms', 'False'),
        ('hs', 'True'),
        ('ns', 'True'),
    )

    OVERLAP_CHOICES = (
        ('ms_partial', 'partial'),
        ('hs_complete', 'complete'),
        ('ns_complete', 'complete'),
    )

class Domain(models.Model):

    DOMAIN_CHOICES = (
        ('bacteria', 'Bacteria'),
        ('archaea', 'Archaea'),
        ('eukarya', 'Eukarya'),
        ('its1', 'ITS1'),
    )

    DOMAIN_SHORTCUTS_CHOICES = (
        ('B', 'Bacteria'),
        ('A', 'Archaea'),
        ('E', 'Eukarya'),
        ('F', 'ITS1'),
    )

    SUITE_DOMAIN_CHOICES = (
        ('B', 'Bacterial'),
        ('A', 'Archaeal'),
        ('E', 'Eukaryal'),
        ('F', 'Fungal'),
    )

    LETTER_BY_DOMAIN_CHOICES = (
        ('bacteria', 'B'),
        ('archaea' , 'A'),
        ('eukarya' , 'E'),
        ('its1'    , 'F'),
    )

    DOMAIN_WITH_LETTER_CHOICES = (
        ('B', 'Bacteria (B)'),
        ('A', 'Archaea (A)' ),
        ('E', 'Eukarya (E)' ),
        ('F', 'ITS1 (ITS1)' ),
    )

class Ill_dna_region(models.Model):

    DNA_REGION_CHOICES = (
        ('v6', 'v6'),
        ('v4v5', 'v4v5'),
        ('v4', 'v4'),
        ('HSSU', 'HSSU'),
        ('HLSU', 'HLSU'),
        ('ITS1', 'ITS1'),
    )

class Has_ns(models.Model):
    HAVING_NS_CHOICES = (
        ('yes', 'Has NNNN in run_key'),
        ('no', 'Does not have NNNN in run_key (NextSeq)'),
    )

class File_name(models.Model):
    FILE_NAME_CHOICES = (
        ('ms', 'MERGED-MAX-MISMATCH-3.unique.nonchimeric.fa'),
        ('hs', 'PERFECT_reads.fa'),
        ('ns', 'MERGED_V6_PRIMERS_REMOVED.unique'),
    )


# # class Forms_model(models.Model):
# #     myDomainChoiceField = models.CharField(blank=True, default='') #max_length=5,
# #     class Meta:
# #         app_label='domain'
#
# class FormsModel(models.Model):
#     domain = models.CharField(max_length=5, blank=True, default='')
#     class Meta:
#         app_label='test'
