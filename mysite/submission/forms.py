from django import forms
#
# class RunForm(forms.Form):
#     find_lane = forms.CharField(label='Lane number', max_length=10)

from .models_l_env454 import Run

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    YEAR_IN_SCHOOL_CHOICES = (
       ('FR', 'Freshman'),
       ('SO', 'Sophomore'),
       ('JR', 'Junior'),
       ('SR', 'Senior'),
    )
    # find_rundate = forms.ChoiceField(YEAR_IN_SCHOOL_CHOICES)
    find_rundate = forms.ModelChoiceField(queryset = Run.objects.filter(run__startswith='201').order_by('-run')[:50], label='Run date', empty_label=None)
    

class ContactForm(forms.Form):
    YEAR_IN_SCHOOL_CHOICES = (
       ('FR', 'Freshman'),
       ('SO', 'Sophomore'),
       ('JR', 'Junior'),
       ('SR', 'Senior'),
    )
    find_rundate = forms.ChoiceField(YEAR_IN_SCHOOL_CHOICES)
  
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class RunForm(forms.Form):
  find_rundate = forms.ModelChoiceField(queryset = Run.objects.order_by('-run')[:10], label='Run date', empty_label=None)
  # find_machine = forms.ModelChoiceField(MACHINE_CHOICES, label='Machine name', empty_label=None)
  # find_domain  = forms.ModelChoiceField(DOMAIN_CHOICES, label='Domain', empty_label=None)
  find_lane    = forms.CharField(label='Lane number', max_length=10)
