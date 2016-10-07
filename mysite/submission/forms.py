from django import forms
from .models_l_env454 import Run, Contact, IlluminaAdaptor, Project, EnvSampleSource
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

    csv_rundate          = forms.CharField(label = 'Run date', max_length = 8,)
    csv_path_to_raw_data = forms.CharField(label = 'Path to raw data', max_length = 128) # <span class="emph">/xraid2-2/sequencing/Illumina/</span>
    csv_platform         = forms.ChoiceField(Machine.PLATFORM_CHOICES, label = 'Platform')
    csv_dna_region       = forms.ChoiceField(Ill_dna_region.DNA_REGION_CHOICES, label = 'DNA Region')
    csv_overlap          = forms.ChoiceField(Overlap.OVERLAP_CHOICES, label = 'Overlap')
    csv_has_ns           = forms.ChoiceField(Has_ns.HAVING_NS_CHOICES, label = 'Has Ns')
    csv_seq_operator     = forms.CharField(label = 'Seq Operator', max_length = 3)
    csv_insert_size      = forms.CharField(label = 'Insert Size', max_length = 3)
    csv_read_length      = forms.CharField(label = 'Read Length', max_length = 3)

class MetadataOutCsvForm(forms.Form):
    # todo: add css class size_number to input
    domain                  = forms.ChoiceField(Domain.DOMAIN_CHOICES, label = '')
    # domain                  = forms.ChoiceField(choices=Domain.DOMAIN_CHOICES)
    lane                    = forms.CharField(label = '', max_length = 1)
    contact_name_query = Contact.objects.all().order_by('last_name')
    contact_name            = forms.ModelChoiceField(queryset = contact_name_query, label = 'Contact Name', empty_label = None, to_field_name = 'contact')
    # to_field_name = "%s, %s" % (last_name, first_name))
    

    #TODO: add N's if needed
    run_key                 = forms.CharField(label = 'Run Key', max_length = 9)
    barcode_index           = forms.CharField(label = 'Barcode Index', max_length = 9)
    adaptor_query = IlluminaAdaptor.objects.all().order_by('illumina_adaptor')
    adaptor                 = forms.ModelChoiceField(queryset = adaptor_query, empty_label = None, to_field_name = 'illumina_adaptor')
    project_query = Project.objects.all().order_by('project')    
    project                 = forms.ModelChoiceField(queryset = project_query, empty_label = None, to_field_name = 'project')
    dataset                 = forms.CharField()
    dataset_description     = forms.CharField()
    env_source_name_query = EnvSampleSource.objects.all().order_by('env_sample_source_id')
    env_source_name         = forms.ModelChoiceField(queryset = env_source_name_query, empty_label = None)
    tubelabel               = forms.CharField()
    barcode                 = forms.CharField()
    amp_operator            = forms.CharField()
