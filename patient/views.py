from django.shortcuts import render,redirect

def home(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    return render(request, 'patient/home.html')

def appointment(request):
    return render (request,'patient_appointment.html')
    
