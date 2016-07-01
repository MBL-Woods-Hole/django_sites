from django import forms
#
# class RunForm(forms.Form):
#     find_lane = forms.CharField(label='Lane number', max_length=10)

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    YEAR_IN_SCHOOL_CHOICES = (
       ('FR', 'Freshman'),
       ('SO', 'Sophomore'),
       ('JR', 'Junior'),
       ('SR', 'Senior'),
    )
    find_rundate = forms.ChoiceField(YEAR_IN_SCHOOL_CHOICES)
    

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
