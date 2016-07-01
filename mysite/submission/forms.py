from django import forms
#
# class RunForm(forms.Form):
#     find_lane = forms.CharField(label='Lane number', max_length=10)

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)