from django.shortcuts import get_object_or_404, render,redirect
from staff.forms import DoctorAvailabilityCreationForm2
from patient.models import Appointment
from django.utils  import timezone
from .models import Doctor
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import DoctorModificationForm


def home(request):
    if 'doctor_id' not in request.session:
        return redirect('staff_login')
    doctor_id = request.session['doctor_id']
    doctor = Doctor.objects.get(id=doctor_id)
    doctor_name = doctor.firstname + ' ' + doctor.lastname
    
    return render(request,'doctor/home.html',{'name':doctor_name})

def doctor_appointment(request):
    if 'doctor_id' not in request.session:
        return redirect('staff_login')
    
    doctor_id = request.session['doctor_id']
    today = timezone.now().date()
    appointments = Appointment.objects.filter(
        doctor_id=doctor_id,
        appointment_date__gte=today
    ).values_list('appointment_date', flat=True)
    
    available_dates_json = [date.strftime('%Y-%m-%d') for date in appointments]
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'doctor/appointment.html', {
        'appointments': available_dates_json,
        'doctor': doctor
    })
def view_appointment(request, date):
    if 'doctor_id' not in request.session:
        return redirect('staff_login')
    doctor_id = request.session['doctor_id']
    appointments = Appointment.objects.filter(
        doctor_id=doctor_id,
        appointment_date=date
    ).select_related('doctor', 'patient')
    
    return render(request, 'doctor/view_appointment.html', {'appointments': appointments, 'date':date})
def doctor_logout(request):
    if 'doctor_id' in request.session:
        request.session.flush()
    return redirect('staff_home')

def edit_doctor_profile(request):
    if 'doctor_id' not in request.session:
        return redirect('staff_login')
    
    doctor_id = request.session['doctor_id']
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        form = DoctorModificationForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_home')
    else:
        form = DoctorModificationForm(instance=doctor)
    
    return render(request, 'doctor/edit_doctor_profile.html', {'form': form})

def create_doctor_availability(request):
    if 'doctor_id' not in request.session:
        return redirect('staff_login')
    doctor_id= request.session['doctor_id']
    
    if request.method == 'POST':
        form = DoctorAvailabilityCreationForm2(request.POST)

        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor_id = doctor_id
            availability.save()
            return redirect('doctor_home')
    else:
        form = DoctorAvailabilityCreationForm2()
        
    return render(request, 'doctor/create_doctor_availability.html', {'form': form,'doctor_id':doctor_id})