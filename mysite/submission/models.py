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
        ('ms', 'MiSeq'),
        ('hs', 'HiSeq'),
        ('ns', 'NextSeq'),
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


class Ill_dna_region(models.Model):

    DNA_REGION_CHOICES = (
        ('v6', 'v6'),
        ('v4v5', 'v4v5'),
        ('v4', 'v4'),
        ('ITS1', 'ITS1'),
    )


class Has_ns(models.Model):
    HAVING_NS_CHOICES = (
        ('yes', 'Has NNNN in run_key'),
        ('no', 'Does not have NNNN in run_key (NextSeq)'),
    )
