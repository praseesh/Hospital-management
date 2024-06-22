from django.shortcuts import render

def home(request):
    return render(request, 'patient/home.html')

def appointment(request):
    return render (request,'patient_appointment.html')
    
