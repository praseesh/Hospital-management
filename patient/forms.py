from django import forms
from .models import Patient

class CustomPatientModification(forms.ModelForm):
    class Meta:
        model = Patient
        # fields = ['firstname', 'lastname', 'mobile', 'email', 'dob', 'gender', 'address', 'admission_date', 'checkout_date']
        fields = '__all__'
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class CustomPatientCreationForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['firstname', 'lastname', 'mobile', 'email', 'dob', 'gender', 'address', 'admission_date']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
        }
        
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if len(mobile) < 10:
            raise forms.ValidationError("Mobile number must be at least 10 digits long.")
        return mobile

    def clean_email(self):
        email = self.cleaned_data['email']
        return email