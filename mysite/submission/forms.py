from django import forms
from django.forms import fields
from .models_l_env454 import Run, Contact, IlluminaAdaptor, Project, EnvSampleSource
from .models import Machine, Domain, Ill_dna_region, Overlap, Has_ns
from django.core.validators import RegexValidator, validate_slug
import datetime
from django.db import models


class RunForm(forms.Form):
    # query = Run.objects.filter(run__startswith = '201').filter(run__gte = '2015').order_by('-run')
    # find_rundate = forms.ModelChoiceField(queryset = query, label = 'Run date', empty_label = None)
    query = Run.cache_all_method.all().filter(run__startswith = '201').filter(run__gte = '2015').order_by('-run')
    find_rundate = forms.ModelChoiceField(queryset = query, label = 'Run date', empty_label = None)
    
    find_machine = forms.ChoiceField(Machine.MACHINE_CHOICES, label = 'Machine name')
    find_domain  = forms.ChoiceField(Domain.DOMAIN_SHORTCUTS_CHOICES, label = 'Domain')
    find_lane    = forms.CharField(label = 'Lane number', max_length = 3)

class FileUploadForm(forms.Form):

    csv_file = forms.FileField()
    print "csv_file from forms.FileUploadForm"
    print csv_file

class CsvRunInfoUploadForm(forms.Form):

    csv_rundate = forms.DateField(label = 'Run date', input_formats = ['%Y%m%d'])
    csv_path_to_raw_data = forms.CharField(label = 'Path to raw data', max_length = 128) # <span class="emph">/xraid2-2/sequencing/Illumina/</span>
    csv_platform         = forms.ChoiceField(Machine.PLATFORM_CHOICES, label = 'Platform')
    csv_dna_region       = forms.ChoiceField(Ill_dna_region.DNA_REGION_CHOICES, label = 'DNA Region')
    csv_overlap          = forms.ChoiceField(Overlap.OVERLAP_CHOICES, label = 'Overlap')
    csv_has_ns           = forms.ChoiceField(Has_ns.HAVING_NS_CHOICES, label = 'Has Ns')
    csv_seq_operator     = forms.CharField(label = 'Seq Operator', max_length = 3)
    csv_insert_size      = forms.IntegerField(label = 'Insert Size', min_value = 1, max_value = 800)
    csv_read_length      = forms.IntegerField(label = 'Read Length', min_value = 1, max_value = 300)
    """
    TODO: add validation
    Min size--must be a positive number
    Max size--for v6, 200; for v4v5, v4, ITS1, 800?  I'm guessing.

    Max read length is 150 on the nextseq and 300 on the Miseq.

    """

class MetadataOutCsvForm(forms.Form):
    # todo: add css class size_number to input
    domain                  = forms.ChoiceField(Domain.DOMAIN_CHOICES, label = '')
    lane                    = forms.IntegerField(max_value = 9, widget=forms.TextInput(attrs={'class': 'size_number'}))
    contact_name_query      = Contact.objects.all().order_by('last_name')
    contact_name            = forms.ModelChoiceField(queryset = contact_name_query, label = 'Contact Name', empty_label = None, to_field_name = 'contact')
    # to_field_name = "%s, %s" % (last_name, first_name))
    # contact_query           = Contact.cache_all_method.all().order_by('contact')
    # contact_name            = forms.ModelChoiceField(queryset = contact_query, label = 'Contact Name', empty_label = None, to_field_name = 'contact')

    #TODO: add N's if needed
    run_key                 = forms.CharField(label = 'Run Key', max_length = 9, widget=forms.TextInput(attrs={'class': 'size_short_input'}))
    barcode_index           = forms.CharField(label = 'Barcode Index', max_length=12, widget=forms.TextInput(attrs={'class': 'size_short_input'}))
    adaptor_query = IlluminaAdaptor.objects.all().order_by('illumina_adaptor')
    adaptor                 = forms.ModelChoiceField(queryset = adaptor_query, to_field_name = 'illumina_adaptor')
    
    project_query = Project.cache_all_method.all().order_by('project')
    # project_query = Project.objects.order_by('project')
    project                 = forms.ModelChoiceField(queryset = project_query, empty_label = None, to_field_name = 'project')
    dataset                 = forms.CharField(min_length=3, max_length=64,
                            validators=[validate_slug])
    dataset_description     = forms.CharField(max_length=100)
    env_source_name_query = EnvSampleSource.objects.all().order_by('env_sample_source_id')
    env_source_name         = forms.ModelChoiceField(queryset = env_source_name_query, empty_label = None)
    tubelabel               = forms.CharField(max_length=32)
    barcode                 = forms.CharField(max_length=12, required=False)
    amp_operator            = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'size_short_input'}))
    
class MonthYearWidget(forms.MultiWidget):
    """
   A widget that splits a date into Month/Year with selects.
   """
    def __init__(self, attrs=None):
        months = (
            ('', 'Month'),
            ('', '---'),
            ('01', 'Jan (01)'),
            ('02', 'Feb (02)'),
            ('03', 'Mar (03)'),
            ('04', 'Apr (04)'),
            ('05', 'May (05)'),
            ('06', 'Jun (06)'),
            ('07', 'Jul (07)'),
            ('08', 'Aug (08)'),
            ('09', 'Sep (09)'),
            ('10', 'Oct (10)'),
            ('11', 'Nov (11)'),
            ('12', 'Dec (12)'),
        )

        year_now = int(datetime.date.today().year)
        year_digits = range(year_now, year_now + 10)
        years = [(year, year) for year in year_digits]
        years.insert(0, ("", "---"))
        years.insert(0, ("", "Year"))

        widgets = (forms.Select(attrs=attrs, choices=months), forms.Select(
            attrs=attrs, choices=years))
        super(MonthYearWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.month, value.year]
        return [None, None]

    def render(self, name, value, attrs=None):
        try:
            value = datetime.date(month=int(
                value[0]), year=int(value[1]), day=1)
        except:
            value = ''

        return super(MonthYearWidget, self).render(name, value, attrs)


class MonthYearField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        """
        Have to pass a list of field types to the constructor, else we
        won't get any data to our compress method.
        """

        all_fields = (
            fields.CharField(),
            fields.CharField(),
        )
        super(MonthYearField, self).__init__(all_fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            s = data_list[0]
            month = int(s) if s else 1
            s = data_list[1]
            year = int(s) if s else datetime.date.today().year

            return datetime.date(year=year, month=month, day=1)
        return None
        
# class NewProjectField(forms.MultiValueField):
#     widget = MonthYearWidget
#
#     def __init__(self, *args, **kwargs):
#         super(NewProjectField, self).__init__(*args, **kwargs)
#         fields = (
#             forms.CharField(),
#             forms.CharField()
#         )
#         """
#         The first part of a project name could have only letters and no more then 4 of them. The second part of a project name could have only letters and numbers and no more then 6 of them
#         domain
#         dna_region
#         """
#
#     def compress(self, data_list):
#         return ' '.join(data_list)


class AddProjectForm(forms.Form):
    project             = MonthYearField()
    project_title       = forms.CharField(min_length=3, max_length=64,
                            validators=[validate_slug])
    project_description = forms.CharField(max_length=100)
    funding             = forms.CharField(max_length=32)
    env_source_name_query = EnvSampleSource.objects.all().order_by('env_sample_source_id')
    env_source_name     = forms.ModelChoiceField(queryset = env_source_name_query, empty_label = None)
    # contact_query       = Contact.cache_all_method.all().order_by('contact')
    # contact             = forms.ModelChoiceField(queryset = contact_query, empty_label = None, to_field_name = 'contact')
    
    contact_name_query  = Contact.objects.all().order_by('last_name')
    contact             = forms.ModelChoiceField(queryset = contact_name_query, label = 'Contact Name', empty_label = None, to_field_name = 'contact')
    
    # def __init__(self, *args, **kwargs):
    #      super(AddProjectForm, self).__init__(self, *args, **kwargs)
    #      self.initial['project'] = ['']

    # class Meta:
    #     model = Project