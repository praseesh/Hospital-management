from django import forms

from staff.models import Invoice
from .models import Patient

class CustomPatientModification(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['firstname', 'lastname', 'mobile', 'email', 'gender', 'address', 'admission_date']
        # fields = '__all__'
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class CustomPatientCreationForm(forms.ModelForm):
    class Meta: 
        model = Patient
        fields = ['firstname', 'lastname','disease', 'mobile', 'email', 'dob', 'gender', 'address', 'admission_date']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            
            
        }
        
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if len(mobile) < 10:
            raise forms.ValidationError("Mobile number must be at least 10 digits long.")
        return mobile

    def clean_email(self):
        email = self.cleaned_data['email']
        return email
    
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields =['patient_id','payment_method','description']