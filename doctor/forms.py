# from django import forms
from django import forms
from .models import Doctor

class DoctorCreationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['firstname', 'lastname', 'specialty', 'email', 'availability', 'contact']

class DoctorModificationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['firstname', 'lastname', 'specialty', 'email', 'availability', 'contact']