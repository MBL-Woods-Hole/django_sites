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


class Domain(models.Model):
    DOMAIN_CHOICES = (
        ('Bacterial', 'Bacteria'),
        ('Archaeal', 'Archaea'),
        ('Eukaryal', 'Eukarya'),
        ('Fungal', 'ITS1'),
    )
