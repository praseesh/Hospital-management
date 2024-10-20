from django.utils import timezone
import json
from django.shortcuts import get_object_or_404, render,redirect
from django.utils.decorators import decorator_from_middleware
from django.contrib import messages
from .forms import CustomPatientCreationForm
from staff.helper import generate_random_string
from .models import Appointment, DoctorAvailability, Patient
from staff.middleware import NoCacheMiddleware
cache_control_no_cache = decorator_from_middleware(NoCacheMiddleware)
from doctor.models import Doctor

# @cache_control_no_cache
def home(request):
    return render(request, 'patient/home.html')

def patient_selection(request):
    if request.method == "POST":
        email = request.POST.get('patient_email')
        if email:
            try:
                patient = Patient.objects.get(email=email)
                return redirect('select_doctor', patient_id=patient.id)
            except Patient.DoesNotExist:
                messages.error(request, 'Patient not found')
                return render(request, 'patient/patient_selection.html')
        else:
            messages.error(request, 'Email not provided')
            return render(request, 'patient/patient_selection.html')
    return render(request, 'patient/patient_selection.html')

def patient_create(request):
    if request.method == 'POST':
        form = CustomPatientCreationForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('select_doctor', patient_id=patient.id)
    else:
        form = CustomPatientCreationForm()
    return render(request, 'patient/patient_create.html', {'form': form})


def select_doctor(request,patient_id): 
    doctor = Doctor.objects.all()
    return render(request, 'patient/select_doctor.html', {'doctor':doctor, 'patient_id':patient_id})
        
def select_date(request, patient_id, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    today = timezone.now().date()
    availability = DoctorAvailability.objects.filter(doctor=doctor, date__gte=today).values('date', 'timeslot')
    
    available_dates = list(availability.values_list('date', flat=True).distinct())
    available_dates_json = json.dumps([str(date) for date in available_dates])
    
    return render(request, 'patient/select_date.html', {
        'doctor': doctor,
        'available_dates_json': available_dates_json,
        'patient_id': patient_id
    })
    
def appointment(request, doctor_id, date,patient_id):    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availability = DoctorAvailability.objects.filter(doctor=doctor, date=date, is_available=True)
    
    if request.method == 'POST':
        timeslot = request.POST.get('timeslot')
        reason = request.POST.get('reason_for_visit')
        rfv = 'other'
        if reason:
           rfv =reason 
        if timeslot and patient_id:
            try:
                make_false = availability.get(timeslot=timeslot)
                make_false.is_available = False
                make_false.save()  
                appointment = Appointment(
                    appointment_id=generate_random_string(),
                    patient_id=patient_id,
                    doctor=doctor,
                    appointment_date=date,
                    timeslot=timeslot,
                    reason_for_visit=rfv
                )
                appointment.save()
                messages.success(request, "Appointment created successfully!")
                return redirect('home')
            except DoctorAvailability.DoesNotExist:
                messages.error(request, "The selected time slot is not available.")
        else:
            messages.error(request, "Please provide all the required details.")
   
    return render(request, 'patient/doctor_availability.html', {
        'doctor': doctor,
        'date': date,
        'availability': availability,
        'patient_id':patient_id
    })