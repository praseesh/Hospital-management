from django.shortcuts import render,redirect
from django.utils.decorators import decorator_from_middleware
from staff.middleware import NoCacheMiddleware
cache_control_no_cache = decorator_from_middleware(NoCacheMiddleware)

@cache_control_no_cache
def home(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    return render(request, 'patient/home.html')

def appointment(request):
    return render (request,'patient_appointment.html')
    
