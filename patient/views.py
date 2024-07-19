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

@cache_control_no_cache
def home(request):
    return render(request, 'patient/home.html')

def patient_selection(request):
    patients = Patient.objects.all()
    patient_name = request.GET.get('patient_name')
    if patient_name != '' and patient_name is not None:
        patient = patient.filter(firstname__icontains = patient_name)

def patient_registration(request):
    patients = Patient.objects.all()
    return render (request, 'patient/registration.html',{'patients':patients})
    

def patient_create(request):
    if request.method =='POST':
        form = CustomPatientCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_patient_list')
    else:
        form = CustomPatientCreationForm()
    return render(request,'patient/patient_create.html', {'form':form})

def select_doctor(request):
    doctor = Doctor.objects.all()
    return render(request, 'staff/select_doctor.html', {'doctor':doctor})
        
def select_date(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availability = DoctorAvailability.objects.filter(doctor=doctor).values('date', 'timeslot')

    available_dates = list(availability.values_list('date', flat=True).distinct())
    available_dates_json = json.dumps([str(date) for date in available_dates])
    return render(request, 'staff/select_date.html', {'doctor': doctor, 'available_dates_json': available_dates_json})

def appointment(request, doctor_id, date):
    if request.method == 'GET':
        print(doctor_id, date)
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availability = DoctorAvailability.objects.filter(doctor=doctor, date=date, is_available=True)
    
    if request.method == 'POST':
        timeslot = request.POST.get('timeslot')
        patient_id = request.POST.get('patient_id')
        patients = Patient.objects.all()
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
    else:
        messages.error(request, "Invalid request method.")
    
    return render(request, 'staff/doctor_availability.html', {
        'doctor': doctor,
        'date': date,
        'availability': availability,
        'patients':patients
    })