from django.shortcuts import render,redirect
from .models import StaffAction, Staff
from django.contrib.auth.hashers import check_password
# Create your views here.

def staff(request):
    actions = None
    if 'staff_id' in request.session:
        staff_id = request.session['staff_id']
        # try:
        staff = Staff.objects.get(id=staff_id)
        actions = StaffAction.objects.filter(role_id=staff.role)
        # except Staff.DoesNotExist:
        #     return render(request, 'staff/staff_login.html', {'message': 'Invalid staff ID'})
        # except Exception:
        #     return render(request, 'staff/staff_login.html', {'message': 'Something went wrong'})
    return render(request, 'staff/home.html', {'actions': actions})

def staff_login(request):
    if request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            staff = Staff.objects.get(email=email)
            if staff is None or staff == '':
                return render(request, 'staff/staff_login.html', {'msg': 'Invalid Email or Password'})
            else:
                # Check password
                if check_password(password, staff.password):
                    request.session['staff_id'] = staff.id
                    return redirect('staff_home')  # Redirect to staff_home view
                else:
                    return render(request, 'staff/staff_login.html', {'msg': 'Invalid Email or Password'})
        except Staff.DoesNotExist:
            return render(request, 'staff/staff_login.html', {'msg': 'Invalid Email or Password'})
    return render(request, 'staff/staff_login.html')
