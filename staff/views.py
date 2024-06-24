
from django.shortcuts import render,redirect, get_object_or_404
from .models import StaffAction, Staff, StaffActionRoles, Invoice, Prescription,ST,SugarTest,CholesterolTest,CT,LiverFunctionTest,LFT,KidneyFunctionTest,KFT
from django.contrib.auth.hashers import check_password
from .forms import LabReportCreation, InvoiceCreationForm, PrescriptionForm,SugarTestForm,CholesterolTestForm,KidneyTestForm, LiverTestForm,CreateRoomForm
from patient.forms import CustomPatientCreationForm,CustomPatientModification
from patient.models import Patient, Room


#<-----------------------------------------STAFF---------------------------------------------------->

def staff(request):
    if 'staff_id' in request.session:
        staff_id = request.session['staff_id']
        staff = Staff.objects.get(id=staff_id)
        
        if staff.role_id ==2:
            actions = StaffAction.objects.all()
        else:
            action_ids = StaffActionRoles.objects.filter(role_id=staff.role_id).values_list('action_id', flat=True)
            actions = StaffAction.objects.filter(id__in=action_ids)
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

#<-------------------------------------------STAFF PATIENT----------------------------------------------->

def staff_patient_create(request):
    if request.method =='POST':
        form = CustomPatientCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_patient_list')
    else:
        form = CustomPatientCreationForm()
    return render(request,'staff/patient_create.html', {'form':form})

def staff_patient_list(request):
    patient = Patient.objects.all()
    patient_name = request.GET.get('patient_name')
    if patient_name != '' and patient_name is not None:
        patient = patient.filter(firstname__icontains = patient_name)
    return render(request, 'staff/patient_list.html', {'patient':patient})

def staff_patient_details(request, patient_id):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    patient = get_object_or_404(Patient, id=patient_id)
    return render (request, 'staff/patient_details.html', {'patient': patient})

def staff_patient_delete(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('staff_patient_list')

def staff_patient_edit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == "POST":
        form = CustomPatientModification(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('staff_patient_list')
    else:
        form = CustomPatientModification(instance=patient)
    
    return render(request, 'staff/patient_edit.html', {'form': form})


#<------------------------------------------PRESCRIPTION----------------------------------------------->

def staff_prescription_create(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')

    staff_id = request.session['staff_id']
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)  
            prescription.created_by = staff_id
            prescription.save()
            return redirect('staff_prescription')
    else:
        form = PrescriptionForm()
    return render(request, 'staff/prescription.html', {'form': form})

def staff_prescription(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    staff_id = request.session['staff_id']
    prescriptions = Prescription.objects.filter(created_by=staff_id).select_related('patient', 'doctor')
    return render(request, 'staff/prescription_list.html', {'prescriptions': prescriptions})

def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription,id=prescription_id)
    prescription.delete()
    return redirect('staff_prescription')
    


#<----------------------------------------------DISCHARGE----------------------------------------------->

def staff_discharge(request):
    return render(request, 'staff/discharge.html')

#<----------------------------------------------DISCHARGE----------------------------------------------->

def staff_appointment(request):
    return render(request, 'staff/appointment.html')




#<------------------------------------------LAB REPORT----------------------------------------------->


def staff_lab_report(request, liver_test_id=None, kidney_test_id=None, sugar_test_id=None, cholesterol_test_id=None):
    if request.method == 'POST':
        form = LabReportCreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_home') 
    else:
        form = LabReportCreation()
    return render(request, 'staff/lab_report.html',{'form':form})

def staff_labreport_create(request):
    if request.method =='POST':
        form = LabReportCreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_lab_report')
    else:
        form = LabReportCreation()
    return render(request, 'staff/lab_report_create.html', {'form':form}) 



def create_cholesterol_test(request):
    if request.method == 'POST':
        form = CholesterolTestForm(request.POST)
        if form.is_valid():
            total_cholesterol = form.cleaned_data.get('total_cholesterol')
            ldl_cholesterol = form.cleaned_data.get('ldl_cholesterol')
            hdl_cholesterol = form.cleaned_data.get('hdl_cholesterol')
            triglycerides = form.cleaned_data.get('triglycerides')
            concatenated_values = f'{total_cholesterol}, {ldl_cholesterol}, {hdl_cholesterol}, {triglycerides}'
            new_cholesterol_test = CholesterolTest.objects.create(result=concatenated_values)
            new_cholesterol_test.save()
            return redirect('staff_lab_report')
        return render(request, 'staff/cholesterol_test.html', {'form': form})
    else:
        form = CholesterolTestForm()
        ct = CT.objects.all()
        return render(request, 'staff/cholesterol_test.html', {'form': form, 'ct': ct})

def create_kidney_test(request):
    if request.method == 'POST':
        form = KidneyTestForm(request.POST)
        if form.is_valid():
            urea_value = form.cleaned_data.get('urea')
            creatinine_value = form.cleaned_data.get('creatinine')
            uric_acid_value = form.cleaned_data.get('uric_acid')
            calcium_total_value = form.cleaned_data.get('calcium_total')
            phosphorus_value = form.cleaned_data.get('phosphorus')
            alkaline_phosphatase_value = form.cleaned_data.get('alkaline_phosphatase')
            total_protein_value = form.cleaned_data.get('total_protein')
            albumin_value = form.cleaned_data.get('albumin')
            sodium_value = form.cleaned_data.get('sodium')
            potassium_value = form.cleaned_data.get('potassium')
            chloride_value = form.cleaned_data.get('chloride')
            
            concatenated_values = f" { urea_value }, { creatinine_value }, { uric_acid_value }, { calcium_total_value }, { phosphorus_value }, { alkaline_phosphatase_value }, { total_protein_value }, { albumin_value }, { sodium_value }, { potassium_value }, { chloride_value } "
            new_kidney_test = KidneyFunctionTest.objects.create(result = concatenated_values)
            new_kidney_test.save()
            return redirect('staff_lab_report')
        
        return render(request, 'staff/kidney_test.html')
    else:
        form = KidneyTestForm()
        kft = KFT.objects.all()
        return render(request, 'staff/kidney_test.html', {'form': form, 'kft': kft})
    


def create_sugar_test(request):
 if request.method =='POST':
    form = SugarTestForm(request.POST)
    if form.is_valid():
        fbs_value = form.cleaned_data.get('fbs')
        pbs_value = form.cleaned_data.get('pbs')
        rbs_value = form.cleaned_data.get('rbs')
        hba1c_value = form.cleaned_data.get('hba1c')
        ogtt_value = form.cleaned_data.get('ogtt')
        concatenated_values = f'{fbs_value}, {pbs_value}, {rbs_value}, {hba1c_value}, {ogtt_value}'
        new_sugar_test = SugarTest.objects.create(result=concatenated_values,)
        new_sugar_test.save()
        return redirect('staff_lab_report')

    return render(request,'staff/sugar_test.html')
 else:
        form = SugarTestForm()
        st = ST.objects.all()
        return render(request, 'staff/sugar_test.html', {'form':form,'st':st}) 

def create_liver_test(request):
    if request.method =='POST':
        form = LiverTestForm(request.POST)
        if form.is_valid():
            total_bilirubin = form.cleaned_data.get('total_bilirubin')
            direct_bilirubin = form.cleaned_data.get('direct_bilirubin')
            indirect_bilirubin = form.cleaned_data.get('indirect_bilirubin')
            ast_sgot= form.cleaned_data.get('ast_sgot')
            alt_sgot = form.cleaned_data.get('alt_sgpt')
            alp= form.cleaned_data.get('alp')
            total_protein= form.cleaned_data.get('total_protein')
            albumin= form.cleaned_data.get('albumin')
            globulin = form.cleaned_data.get('globulin')
            albumin_globulin_ratio = form.cleaned_data.get('albumin_globulin_ratio')
            
            concatenated_values = f"{ total_bilirubin }, {direct_bilirubin}, { indirect_bilirubin }, { ast_sgot }, {alt_sgot}, { alp }, { total_protein }, { albumin }, { globulin } { albumin_globulin_ratio }"
            new_lft = LiverFunctionTest.objects.create(result = concatenated_values)
            new_lft.save()
            return redirect('staff_lab_report')
        return render(request,'staff/liver_test.html')
    else:
        form = LiverTestForm()
        lft = LFT.objects.all()
        return render(request, 'staff/liver_test.html', {'form': form, 'lft':lft})
    


#<------------------------------------------INVOICE----------------------------------------------->


def staff_invoice(request):
    if request.method =='POST':
        return redirect('staff_login')
    
    
    return render(request,'staff/invoice.html')

#<----------------------------------------------ROOMS----------------------------------------------->

def staff_rooms(request):
    if request.method == "GET":
        room_no = request.GET.get('search')
        rooms = Room.objects.filter(room_number__icontains=room_no) if room_no else Room.objects.all()
        context = {'rooms': rooms, 'room_no': room_no}
        return render(request, 'staff/rooms.html', context)

def create_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_rooms')
    else:
        form = CreateRoomForm()
    return render(request, 'staff/create_rooms.html', {'form': form})


def assign_patient(request,room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method=="POST":
        patient_id = request.POST.get('patient_id')
        
        if not room.is_vacant:
            error_message = "This room is already occupied."
            return render(request, 'staff/assign_patient.html', {'message': error_message, 'room_id': room_id})
        
        updated = Patient.objects.filter(id=patient_id).update(room_id=room_id)
        room_update = Room.objects.filter(id=room_id).update(is_vacant=False)
        if updated:
            return redirect('staff_rooms')
        else:
            error_message = "Patient does not exist."

        return render(request, 'staff/assign_patient.html', {'message': error_message, 'room_id': room_id})

    return render(request, 'staff/assign_patient.html', {'room_id': room_id})
    
    
    
    
    
    
# https://www.dbdiagram.io/d/Hospital-Management-665befbcb65d933879443c64