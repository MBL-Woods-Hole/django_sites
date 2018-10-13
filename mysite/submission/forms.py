from django import forms
from django.forms import fields

from .models_l_env454 import Run as models_run, Contact, IlluminaAdaptor, Project, EnvSampleSource
from .model_choices import Machine, Domain, Ill_dna_region, Overlap, Has_ns, Db_name
from django.core.validators import RegexValidator, validate_slug
import datetime
from django.db import models


class RunForm(forms.Form):
    # query = Run.objects.filter(run__startswith = '201').filter(run__gte = '2015').order_by('-run')
    # find_rundate = forms.ModelChoiceField(queryset = query, label = 'Run date', empty_label = None)
    query = models_run.cache_all_method.all().filter(run__startswith = '201').filter(run__gte = '2015').order_by('-run')
    find_rundate = forms.ModelChoiceField(queryset = query, label = 'Run date', empty_label = None)

    find_machine = forms.ChoiceField(choices = Machine.MACHINE_CHOICES, label = 'Machine name')
    find_domain = forms.ChoiceField(choices = Domain.DOMAIN_SHORTCUTS_CHOICES, label = 'Domain')
    find_lane = forms.CharField(label = 'Lane number', max_length = 3)
    find_db_name = forms.ChoiceField(choices = Db_name.DB_NAME_CHOICES, label = 'Database name')


class FileUploadForm(forms.Form):
    csv_file = forms.FileField()
    # print "csv_file from forms.FileUploadForm"
    # print csv_file


class CsvRunInfoUploadForm(forms.Form):
    csv_rundate = forms.DateField(label = 'Run date', input_formats = ['%Y%m%d'])
    csv_path_to_raw_data = forms.CharField(label = 'Path to raw data', max_length = 128, widget = forms.TextInput(
        attrs = {'id': 'path_ext_msg'}))  # <span class="emph">/xraid2-2/sequencing/Illumina/</span>
    csv_platform = forms.ChoiceField(choices = Machine.PLATFORM_CHOICES, label = 'Platform')
    csv_dna_region = forms.ChoiceField(choices = Ill_dna_region.DNA_REGION_CHOICES, label = 'DNA Region')
    csv_overlap = forms.ChoiceField(choices = Overlap.OVERLAP_CHOICES, label = 'Overlap')
    csv_has_ns = forms.ChoiceField(choices = Has_ns.HAVING_NS_CHOICES, label = 'Has Ns')
    csv_seq_operator = forms.CharField(label = 'Seq Operator', max_length = 3)
    csv_insert_size = forms.IntegerField(label = 'Insert Size', min_value = 1, max_value = 800)
    csv_read_length = forms.IntegerField(label = 'Read Length', min_value = 1, max_value = 300)
    """
    TODO: add validation
    Min size--must be a positive number
    Max size--for v6, 200; for v4v5, v4, ITS1, 800?  I'm guessing.

    Max read length is 150 on the nextseq and 300 on the Miseq.

    """


class MetadataOutCsvForm(forms.Form):
    # todo: add css class size_number to input
    domain = forms.ChoiceField(choices = Domain.DOMAIN_CHOICES, label = '')
    lane = forms.IntegerField(max_value = 9, widget = forms.TextInput(attrs = {'class': 'size_number'}))
    # contact_name_query      = Contact.objects.all().order_by('last_name')
    contact_name_query = Contact.cache_all_method.all().order_by('contact')
    contact_name = forms.ModelChoiceField(queryset = contact_name_query, label = 'Contact Name', empty_label = None,
                                          to_field_name = 'contact')
    # to_field_name = "%s, %s" % (last_name, first_name))

    # TODO: add N's if needed
    run_key = forms.CharField(label = 'Run Key', max_length = 9,
                              widget = forms.TextInput(attrs = {'class': 'size_short_input'}))
    barcode_index = forms.CharField(label = 'Barcode Index', max_length = 12,
                                    widget = forms.TextInput(attrs = {'class': 'size_short_input'}))

    adaptor_query = IlluminaAdaptor.cache_all_method.all().order_by('illumina_adaptor')
    # adaptor_query = IlluminaAdaptor.objects.all().order_by('illumina_adaptor')
    adaptor = forms.ModelChoiceField(queryset = adaptor_query, to_field_name = 'illumina_adaptor')

    project_query = Project.cache_all_method.all().order_by('project')
    # project_query = Project.objects.order_by('project')
    project = forms.ModelChoiceField(queryset = project_query, empty_label = None, to_field_name = 'project')
    dataset = forms.CharField(min_length = 3, max_length = 64,
                              validators = [validate_slug])
    dataset_description = forms.CharField(max_length = 100)
    # env_source_name_query = EnvSampleSource.objects.all().order_by('env_sample_source_id')
    env_source_name_query = EnvSampleSource.cache_all_method.all().order_by('env_sample_source_id')
    env_source_name = forms.ModelChoiceField(queryset = env_source_name_query, empty_label = None)
    tubelabel = forms.CharField(max_length = 32)
    barcode = forms.CharField(max_length = 12, required = False)
    amp_operator = forms.CharField(max_length = 5, widget = forms.TextInput(attrs = {'class': 'size_short_input'}))

    # lane                    = forms.IntegerField(max_value = 9, widget=forms.TextInput(attrs={'class': 'size_number'}))


class PhoneField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        # Define one message for all fields.
        error_messages = {
            'incomplete': 'Enter a country calling code and a phone number.',
        }
        # Or define a different message for each field.
        fields = (
            forms.CharField(
                error_messages = {'incomplete': 'Enter a country calling code.'},
                validators = [
                    RegexValidator(r'^[0-9]+$', 'Enter a valid country calling code.'),
                ],
            ),
            forms.CharField(
                error_messages = {'incomplete': 'Enter a phone number.'},
                validators = [RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')],
            ),
            forms.CharField(
                validators = [RegexValidator(r'^[0-9]+$', 'Enter a valid extension.')],
                required = False,
            ),
        )
        super(PhoneField, self).__init__(
            error_messages = error_messages, fields = fields,
            require_all_fields = False, *args, **kwargs
        )


class ComplexMultiWidget(forms.MultiWidget):
    def __init__(self, attrs = None):
        widgets = (
            forms.TextInput(attrs = {'class': 'size_short_input'}),
            forms.TextInput(attrs = {'class': 'size_short_input'}),
            forms.widgets.Select(choices = Domain.DOMAIN_WITH_LETTER_CHOICES),
            forms.widgets.Select(choices = Ill_dna_region.DNA_REGION_CHOICES),
        )
        super(ComplexMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            data = value.split('_')
            return [data[0], data[1], data[2], data[3]]
        return [None, None, None, None]

    def format_output(self, rendered_widgets):
        return u'\n'.join(rendered_widgets)


# http://stackoverflow.com/questions/2386541/creating-a-custom-django-form-field-that-uses-two-inputs
# Please choose a valid env_source_name
class ComplexField(forms.MultiValueField):
    def __init__(self, required = True, widget = None, label = None, initial = None):
        fields = (
            # forms.CharField(validators=[RegexValidator('^[A-Za-z]+$'), message = "The first part of a project name could have only letters"], max_length = 4, error_messages={'max_length': 'The first part of a project name could have no more then 4 of characters.'}),
            forms.CharField(validators = [
                RegexValidator('^[A-Za-z]+$', message = "The first part of a project name could have letters only")],
                            max_length = 4, error_messages = {
                    'max_length': 'The first part of a project name could have no more then 4 characters'
                }),

            forms.CharField(validators = [RegexValidator('^[A-Za-z0-9]+$',
                                                         message = "The second part of a project name could have only letters and numbers")],
                            max_length = 6, error_messages = {
                    'max_length': 'The second part of a project name could have no more then 6 characters'
                }),

            forms.ChoiceField(choices = Domain.DOMAIN_WITH_LETTER_CHOICES),
            forms.ChoiceField(choices = Ill_dna_region.DNA_REGION_CHOICES),
        )
        super(ComplexField, self).__init__(fields, required = required,
                                           widget = widget, label = label, initial = initial)

        # name.validators[-1].message = 'Your question is too long.'

    def compress(self, data_list):
        if data_list:
            return '%s' % ('_'.join(data_list))
        return None


class AddProjectForm(forms.Form):
    project = ComplexField(widget = ComplexMultiWidget())
    project_title = forms.CharField(min_length = 3, max_length = 64,
                                    validators = [RegexValidator('^[A-Za-z0-9_ -]+$',
                                                                 message = "Enter a project title consisting of letters, numbers, underscores, hyphens or spaces")])
    # validators=[validate_slug])
    project_description = forms.CharField(max_length = 100)
    funding = forms.CharField(max_length = 32)
    env_source_name_query = EnvSampleSource.cache_all_method.all().order_by('env_sample_source_id')
    env_source_name = forms.ModelChoiceField(queryset = env_source_name_query, empty_label = None, )
    # http://stackoverflow.com/questions/22886411/validation-errors-on-modelchoicefield
    # https://snakeycode.wordpress.com/2015/02/11/django-dynamic-modelchoicefields/comment-page-1/
    # validators=[RegexValidator('^[A-Za-z0-9]+$', message="The second part of a project name could have only letters and numbers")]
    # Please choose a valid env_source_name
    contact_query = Contact.cache_all_method.all().order_by('last_name')
    contact = forms.ModelChoiceField(queryset = contact_query, empty_label = None, to_field_name = 'contact')

    # contact_name_query  = Contact.objects.all().order_by('last_name')
    # contact             = forms.ModelChoiceField(queryset = contact_name_query, label = 'Contact Name', empty_label = None, to_field_name = 'contact')


class ChooseProjectNOwnerForm(forms.Form):
    project_query = Project.cache_all_method.all().order_by('project')
    project = forms.ModelChoiceField(queryset = project_query, empty_label = None, to_field_name = 'project')
    contact_query = Contact.cache_all_method.all().order_by('last_name')
    contact = forms.ModelChoiceField(queryset = contact_query, empty_label = None, to_field_name = 'contact')
