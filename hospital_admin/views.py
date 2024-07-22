from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.hashers import check_password
from .models import Admin
from staff.models import Staff
from doctor.models import Doctor 
from patient.models import Patient
from doctor.forms import DoctorModificationForm,DoctorCreationForm
from staff.forms import CustomStaffCreation,CustomStaffModification
from patient.forms import CustomPatientModification,CustomPatientCreationForm
# from django.contrib.auth.hashers import make_password


def admin_login(request):
    if 'admin_email' in request.session:
        return redirect('admin_home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # name = 'Praseesh'
        # admin = Admin(
        #     name=name,
        #     email=email,
        #     password= make_password(password)
        # )
        # admin.save()
        try:
            admin = Admin.objects.get(email=email)
            if admin is None or admin is '':
                return render(request,'hospital_admins/login.html',{'msg':'Invalid email or password'})
            if check_password(password,admin.password):
                request.session['admin_email']= email
                request.session.set_expiry(3000)
                return redirect('admin_home')
            return render(request,'hospital_admins/login.html',{'msg':'Invalid email or password'})
        except Exception as e:
            return render(request,'hospital_admins/login.html',{'msg':e})
    return render(request,'hospital_admins/login.html')
    
def home(request):
    if 'admin_email' in request.session:
        return redirect('admin_home')
    if request.method == 'GET':
        return render(request,'hospital_admins/home.html')
    return redirect('login')

def logout(request):
    if request.method == 'POST':
        if 'admin_email' in request.session:
            request.session.flush()
            return redirect('login')
    return redirect('login')

#  <---------------------------------------------DOCTOR SECTION---------------------------------------------->

def doctor_create(request):
    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        
        #email extract
        #check that email existing on staff 
        # get staff by email
        # if staff object not none then give error message
        # if that give error message like can't use this email
        
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorCreationForm()
    return render(request, 'hospital_admins/doctor_create.html', {'form': form } )

def doctor_list(request):
    doctors = Doctor.objects.all()
    doc_name = request.GET.get('doc_name')
    if doc_name:
        doctors = doctors.filter(firstname__icontains=doc_name)
    return render(request, 'hospital_admins/doctor.html', {'doctors': doctors})

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'hospital_admins/doctor_detail.html', {'doctor': doctor})

def doctor_edit(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == "POST":
        form = DoctorModificationForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_detail', doctor_id=doctor.id)
    else:
        form = DoctorModificationForm(instance=doctor)
    return render(request, 'hospital_admins/patient_edit.html', {'form': form})

def doctor_delete(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect('doctor_list')



#  <-------------------------------------------STAFF SECTION-------------------------------------------->

def staff_list(request):
    staff = Staff.objects.all()
    staff_name = request.GET.get('staff_name')
    
    if staff_name != '' and staff_name is not None:
        staff = staff.filter(firstname__icontains=staff_name)
    return render(request, 'hospital_admins/staff.html', {'staff':staff})

def staff_create(request):
    if request.method=='POST':
        form = CustomStaffCreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = CustomStaffCreation()
    return render(request, 'hospital_admins/staff_create.html', {'form':form})

def staff_details(request,staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    return render(request, 'hospital_admins/staff_detail.html',{'staff':staff})

def staff_edit(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method=="POST":
        form = CustomStaffModification(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_detail', staff_id=staff_id)
    else:
        form = CustomStaffModification(instance=staff)
    return render(request, 'hospital_admins/staff_edit.html', {'form':form})

def staff_delete(request,staff_id):
    form = get_object_or_404(Staff, id=staff_id)
    form.delete()
    return redirect('staff_list')

def deleted_staff_list(request):
    deleted_staff = Staff.deleted_objects.all()
    return render(request, 'hospital_admins/deleted_staff_list.html', {'deleted_staff': deleted_staff})

#  <---------------------------------------PATIENT SECTION---------------------------------------------->

def patient_list(request):
    patient = Patient.objects.all()
    patient_name = request.GET.get('patient_name')
    if patient_name != '' and patient_name is not None:
        patient = patient.filter(firstname__icontains = patient_name)
    return render (request, 'hospital_admins/patient.html', {'patient': patient})


def patient_edit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == "POST":
        form = CustomPatientModification(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient_id)
    else:
        form = CustomPatientModification(instance=patient)
    return render(request, 'hospital_admins/patient_edit.html', {'form': form, 'patient_id': patient_id})

def patient_details(request,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'hospital_admins/patient_details.html',{'patient':patient} )


def patient_create(request):
    if request.method =='POST':
        form = CustomPatientCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = CustomPatientCreationForm()
    return render (request,'hospital_admins/patient_create.html',{'form':form})

def patient_delete(request, patient_id):
    patient = get_object_or_404(Patient,id = patient_id)
    patient.delete()
    return redirect('patient_list')



                