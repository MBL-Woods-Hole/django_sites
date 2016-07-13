from django import forms
from .models_l_env454 import Run
from .models import Machine, Domain, Ill_dna_region, Overlap, Has_ns


class RunForm(forms.Form):
    query = Run.objects.filter(run__startswith = '201').filter(run__gte = '2015').order_by('-run')
    find_rundate = forms.ModelChoiceField(queryset = query, label = 'Run date', empty_label = None)
    find_machine = forms.ChoiceField(Machine.MACHINE_CHOICES, label = 'Machine name')
    find_domain  = forms.ChoiceField(Domain.DOMAIN_SHORTCUTS_CHOICES, label = 'Domain')
    find_lane    = forms.CharField(label = 'Lane number', max_length = 3)

class FileUploadForm(forms.Form):

    csv_file = forms.FileField()
    print "csv_file from forms.FileUploadForm"
    print csv_file

class CsvRunInfoUploadForm(forms.Form):

    find_rundate          = forms.CharField(label = 'Run date', max_length = 8,)
    find_path_to_raw_data = forms.CharField(label = 'Path to raw data <span class="emph">/xraid2-2/sequencing/Illumina/</span>', max_length = 12)
    find_dna_region       = forms.ChoiceField(Ill_dna_region.DNA_REGION_CHOICES, label = 'DNA Region')
    find_overlap          = forms.ChoiceField(Overlap.OVERLAP_CHOICES, label = 'Overlap')
    find_has_ns           = forms.ChoiceField(Has_ns.HAVING_NS_CHOICES, label = 'Has Ns')
    find_seq_operator     = forms.CharField(label = 'Seq Operator', max_length = 3)
    find_insert_size      = forms.CharField(label = 'Insert Size', max_length = 3)
    find_read_length      = forms.CharField(label = 'Read Length', max_length = 3)
