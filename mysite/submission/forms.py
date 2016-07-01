from django import forms
from .models_l_env454 import Run
from .models import Machine, Domain


class NameForm(forms.Form):
#   find_rundate = forms.ModelChoiceField(queryset = Run.objects.filter(run__gte='2014').order_by('-run')
# , label='Run date', empty_label=None)
  query = Run.objects.filter(run__gte='2015').filter(run__startswith='201').order_by('-run')
  find_rundate = forms.ModelChoiceField(queryset = query, label='Run date', empty_label=None)
  find_machine = forms.ChoiceField(Machine.MACHINE_CHOICES, label='Machine name')
  find_domain  = forms.ChoiceField(Domain.DOMAIN_CHOICES, label='Domain')
  find_lane    = forms.CharField(label='Lane number', max_length=10)

    # your_name = forms.CharField(label='Your name', max_length=100)
    # YEAR_IN_SCHOOL_CHOICES = (
    #    ('FR', 'Freshman'),
    #    ('SO', 'Sophomore'),
    #    ('JR', 'Junior'),
    #    ('SR', 'Senior'),
    # )
    # # find_rundate = forms.ChoiceField(YEAR_IN_SCHOOL_CHOICES)
    # find_rundate = forms.ModelChoiceField(queryset = Run.objects.filter(run__startswith='201').order_by('-run')[:50], label='Run date', empty_label=None)
    # find_machine = forms.ChoiceField(Machine.MACHINE_CHOICES, label='Machine name')

class RunForm(forms.Form):
  # book = forms.ModelChoiceField(queryset = Book.objects.filter(pk__in = Book.objects.order_by('-rating')[:100].values_list('pk')))

  # find_rundate = forms.ModelChoiceField(queryset = Run.objects.filter(pk__in = Run.objects.filter(run__startswith='201').order_by('-run')[:50].values_list('pk')))

  query = Run.objects.filter(run__gte='2015').filter(run__startswith='201').order_by('-run')
  find_rundate = forms.ModelChoiceField(queryset =query, label='Run date', empty_label=None)
  find_machine = forms.ChoiceField(Machine.MACHINE_CHOICES, label='Machine name')
  find_domain  = forms.ChoiceField(Domain.DOMAIN_CHOICES, label='Domain')
  find_lane    = forms.CharField(label='Lane number', max_length=3)
