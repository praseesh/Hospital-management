from .models import Medicine, PatientBills, Staff, LabReport, Prescription,SugarTest,Invoice
from patient.models import Patient, Room,Appointment
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
    # class Meta:
    #     model = LabReport
    #     fields = ['category','patient', 'doctor', 'date', 'amount', 'result', 'kidney_test', 'liver_test', 'sugar_test', 'cholesterol_test']
    #     widgets = {
    #         'date': forms.DateInput(attrs={'type': 'date'}),
    #     }
    class Meta:
        model = LabReport
        fields = ['category', 'patient', 'doctor', 'date', 'amount', 'result', 'kidney_test', 'liver_test', 'sugar_test', 'cholesterol_test']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'category': 'Category',
            'patient': 'Patient',
            'doctor': 'Doctor',
            'date': 'Date',
            'amount': 'Amount',
            'result': 'Result',
            'kidney_test': 'Kidney Test',
            'liver_test': 'Liver Test',
            'sugar_test': 'Sugar Test',
            'cholesterol_test': 'Cholesterol Test',
        }

    def clean_date(self):
        date = self.cleaned_data['date']

        return date

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'doctor', 'medication', 'dosage', 'frequency', 'duration', 'instructions']
        
class SugarTestForm(forms.Form):
    fbs	 = forms.CharField(max_length=50)
    pbs	 = forms.CharField(max_length=50)
    rbs	 = forms.CharField(max_length=50)
    hba1c= forms.CharField(max_length=50)
    ogtt = forms.CharField(max_length=50)
    class Meta:
        fields = ['result']


class KidneyTestForm(forms.Form):
    urea                 = forms.CharField(max_length=50)
    creatinine           = forms.CharField(max_length=50)
    uric_acid            = forms.CharField(max_length=50)
    calcium_total        = forms.CharField(max_length=50)
    phosphorus           = forms.CharField(max_length=50)
    alkaline_phosphatase = forms.CharField(max_length=50)
    total_protein        = forms.CharField(max_length=50)
    albumin              = forms.CharField(max_length=50)
    sodium               = forms.CharField(max_length=50)
    potassium            = forms.CharField(max_length=50)
    chloride             = forms.CharField(max_length=50)

    class Meta:
        fields = ['result']
        
class CholesterolTestForm(forms.Form):
    total_cholesterol = forms.CharField(max_length=50)
    ldl_cholesterol   = forms.CharField(max_length=50)
    hdl_cholesterol   = forms.CharField(max_length=50)
    triglycerides     = forms.CharField(max_length=50)

    class Meta:
        fields = ['result']
        
class LiverTestForm(forms.Form):
    total_bilirubin        = forms.CharField(max_length=50)
    direct_bilirubin       = forms.CharField(max_length=50)
    indirect_bilirubin     = forms.CharField(max_length=50)
    ast_sgot               = forms.CharField(max_length=50)
    alt_sgpt               = forms.CharField(max_length=50)
    alp                    = forms.CharField(max_length=50)
    total_protein          = forms.CharField(max_length=50)
    albumin                = forms.CharField(max_length=50)
    globulin               = forms.CharField(max_length=50)
    albumin_globulin_ratio = forms.CharField(max_length=50)

    class Meta:
        fields = ['result']
        
        
class InvoiceCreationForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        
class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number','room_type','price' ]
        
class RoomAssignForm(forms.ModelForm):
     class Meta:
        model = Patient
        fields = ['id']    
        
class MedicineBillCreationForm(forms.ModelForm):
    # patient_id = forms.IntegerField()

    class Meta:
        model = PatientBills
        fields = ['patient']
        
class AppointmentCreationForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'reason_for_visit']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }