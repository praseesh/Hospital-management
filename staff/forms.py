from .models import Medicine, PatientBills, Staff, LabReport, Prescription,SugarTest,Invoice
from patient.models import Patient, Room,Appointment, DoctorAvailability
from django import forms
from django.contrib.auth.hashers import make_password


class OTPValidationForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(max_length=6)

class OTPForm(forms.Form):
    email = forms.EmailField()


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
        fields = ['patient', 'doctor', 'result']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'patient': 'Patient',
            'doctor': 'Doctor',
            'amount': 'Amount',
            'result': 'Result',
        }

    def clean_date(self):
        date = self.cleaned_data['date']

        return date

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'doctor', 'medication', 'dosage', 'frequency', 'duration', 'instructions']
        
class SugarTestForm(forms.Form):
    fbs	 = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    pbs	 = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    rbs	 = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    hba1c= forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    ogtt = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    class Meta:
        fields = ['fbs','pbs', 'rbs', 'hba1c', 'ogtt']


class KidneyTestForm(forms.Form):
    urea = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    creatinine = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    uric_acid = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    calcium_total = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    phosphorus = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    alkaline_phosphatase = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    total_protein = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    albumin = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    sodium = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    potassium = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))
    chloride = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': '0'}))

    class Meta:
        fields = [
            'urea',
            'creatinine',
            'uric_acid',
            'calcium_total',
            'phosphorus',
            'alkaline_phosphatase',
            'total_protein',
            'albumin',
            'sodium',
            'potassium',
            'chloride'
        ]
        
class CholesterolTestForm(forms.Form):
    total_cholesterol = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    ldl_cholesterol   = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    hdl_cholesterol   = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    triglycerides     = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))

    class Meta:
        fields = ['total_cholesterol', 'ldl_cholesterol','hdl_cholesterol','triglycerides']
        
class LiverTestForm(forms.Form):
    
    total_bilirubin        = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    direct_bilirubin       = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    indirect_bilirubin     = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    ast_sgot               = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    alt_sgpt               = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    alp                    = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    total_protein          = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    albumin                = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    globulin               = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))
    albumin_globulin_ratio = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min':'0'}))

    class Meta:
        fields = [
            'total_bilirubin',
            'direct_bilirubin',
            'indirect_bilirubin',
            'ast_sgot',
            'alt_sgpt',
            'alp',
            'total_protein',
            'albumin',
            'globulin',
            'albumin_globulin_ratio']
        
        
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

    class Meta:
        model = PatientBills
        fields = ['patient']
        
class AppointmentCreationForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'timeslot', 'reason_for_visit']

class DoctorAvailabilityCreationForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['doctor', 'date', 'timeslot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['timeslot'].choices = Appointment.TIMESLOT_LIST

    def clean_timeslot(self):
        timeslot_key = self.cleaned_data['timeslot']
        timeslot_dict = dict(Appointment.TIMESLOT_LIST)
        timeslot_key=timeslot_key
        if timeslot_key in timeslot_dict.keys():
            return timeslot_dict[timeslot_key]
        else:
            raise forms.ValidationError("Invalid timeslot selection.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.timeslot = self.cleaned_data['timeslot']
        if commit:
            instance.save()
        return instance