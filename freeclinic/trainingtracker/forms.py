from django.forms import forms

class SettingsForm(forms.Form):
    username = forms.CharField(label='Username: ', max_length = 100, required=False)
    email = forms.CharField(label='Email: ', max_length = 100, required=False)
    fname = forms.CharField(label='First name: ', max_length = 50, required=False)
    lname = forms.CharField(label='Last name: ', max_length = 50, required=False)