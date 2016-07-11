from django import forms
from .models_l_env454 import Run
from .models import Machine, Domain


class RunForm(forms.Form):
    query = Run.objects.filter(run__startswith = '201').filter(run__gte = '2015').order_by('-run')
    find_rundate = forms.ModelChoiceField(queryset = query, label = 'Run date', empty_label = None)
    find_machine = forms.ChoiceField(Machine.MACHINE_CHOICES, label = 'Machine name')
    find_domain  = forms.ChoiceField(Domain.DOMAIN_SHORTCUTS_CHOICES, label = 'Domain')
    find_lane    = forms.CharField(label = 'Lane number', max_length = 3)

class CodeUploadForm(forms.Form):

    my_file = forms.FileField()
    print "my_file from forms.CodeUploadForm"
    print my_file
    # place = forms.ModelChoiceField(queryset=Incentive.objects.all())
