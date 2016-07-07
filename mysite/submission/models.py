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
    
class Overlap(models.Model):
    COMPLETE_OVERLAP_CHOICES = (
        ('ms', 'False'),
        ('hs', 'True'),
        ('ns', 'True'),
    )
    

class Domain(models.Model):
    # DOMAIN_CHOICES = (
    #     ('Bacterial', 'Bacteria'),
    #     ('Archaeal',  'Archaea'),
    #     ('Eukaryal',  'Eukarya'),
    #     ('Fungal',    'ITS1'),
    # )

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