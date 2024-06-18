from .models import Staff, LabReport
from django import forms
from django.contrib.auth.hashers import make_password

class CustomStaffCreation(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['firstname','lastname','role', 'city', 'joined', 'salary', 'contact', 'password','email']
    def save(self, commit=True):
        staff = super().save(commit=False)
        staff.password = make_password(self.cleaned_data['password'])
        if commit:
            staff.save()
        return staff
        
class CustomStaffModification(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['firstname', 'lastname','role', 'contact','email'] 
        
class LabReportCreation(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = ['category','patient', 'doctor', 'date', 'amount', 'remarks', 'result']