from django.shortcuts import render,redirect
from .models import StaffAction, Staff
from django.contrib.auth.hashers import check_password
# Create your views here.

# def staff(request):
#     actions = None
#     if 'staff_id' in request.session:
#         staff_id = request.session['staff_id']
#         # try:
#         staff = Staff.objects.get(id=staff_id)
#         if staff.role_id==3:
#             actions=StaffAction.objects.filter(id__lte=24)
#         else:
#             actions = StaffAction.objects.filter(role_id=staff.role)
#         # except Staff.DoesNotExist:
#         #     return render(request, 'staff/staff_login.html', {'message': 'Invalid staff ID'})
#         # except Exception:
#         #     return render(request, 'staff/staff_login.html', {'message': 'Something went wrong'})
#     return render(request, 'staff/home.html', {'actions': actions})

def staff(request):
    if 'staff_id' in request.session:
        staff_id = request.session['staff_id']
        staff = Staff.objects.get(id=staff_id)
        if staff.role_id ==2:
            actions = StaffAction.objects.all()
        elif staff.role_id == 13:
            actions = StaffAction.objects.filter(id__lte=24)
        else:
            actions = StaffAction.objects.filter(role_id=staff.role_id)
        if not actions.exists():
            actions = StaffAction.objects.all()

        return render(request, 'staff/home.html', {'actions': actions})
    
    return render(request, 'staff/staff_login.html')
def staff_login(request):
    if request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            staff = Staff.objects.get(email=email)
            if staff is None or staff == '':
                return render(request, 'staff/staff_login.html', {'msg': 'Invalid Email or Password'})
            else:
                if check_password(password, staff.password):
                    request.session['staff_id'] = staff.id
                    return redirect('staff_home') 
                else:
                    return render(request, 'staff/staff_login.html', {'msg': 'Invalid Email or Password'})
        except Staff.DoesNotExist:
            return render(request, 'staff/staff_login.html', {'msg': 'Invalid Email or Password'})
    return render(request, 'staff/staff_login.html')


def staff_doctor_list(request):

    return render(request, 'staff/doctor_list.html')

def staff_patient_list(request):

    return render(request, 'staff/patient_list.html')

def staff_invoice(request):
    return render(request,'staff/invoice.html')

def staff_lab_report(request):
    return render(request, 'staff/lab_report.html')

def staff_prescription(request):
    return render (request, 'staff/prescription.html')

def staff_rooms(request):
    return render (request,'staff/rooms.html')

def staff_discharge(request):
    return render(request, 'staff/discharge.html')

def staff_appointment(request):
    return render(request, 'staff/appointment.html')