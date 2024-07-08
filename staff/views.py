from decimal import Decimal
import json
import os
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from doctor.models import Doctor
from .models import LabReport, StaffAction, Staff, StaffActionRoles, Invoice, Prescription, ST, SugarTest, CholesterolTest, CT, LiverFunctionTest, LFT, KidneyFunctionTest, KFT, Medicine, PatientBills
from django.contrib.auth.hashers import check_password
from .forms import AppointmentCreationForm, DischargeForm, DoctorAvailabilityCreationForm, LabReportCreation, InvoiceCreationForm, MedicineBillCreationForm, OTPForm, PrescriptionForm, SugarTestForm, CholesterolTestForm, KidneyTestForm, LiverTestForm, CreateRoomForm
from patient.forms import CustomPatientCreationForm, CustomPatientModification, InvoiceForm
from patient.models import Appointment, DoctorAvailability, Patient, Room
from .helper import generate_random_string, generate_otp
from django.urls import reverse, reverse_lazy
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .paypal_config import *
from reportlab.pdfgen import canvas
from .forms import OTPValidationForm
from .models import UserOTP
from django.utils import timezone
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from .middleware import NoCacheMiddleware
from django.utils.decorators import decorator_from_middleware
from django.views.generic import ListView,CreateView
cache_control_no_cache = decorator_from_middleware(NoCacheMiddleware)

"""<__________________________________________STAFF______________________________________________>"""

@cache_control_no_cache
def staff(request):
    staff_id = request.session.get('staff_id')
    
    if not staff_id:
        return redirect('staff_login')
    try:
        staff = Staff.objects.get(id=staff_id)
    except Staff.DoesNotExist:

        return redirect('staff_login')  
    
    if staff.role_id == 2:
        actions = StaffAction.objects.all()
    else:
        action_ids = StaffActionRoles.objects.filter(role_id=staff.role_id).values_list('action_id', flat=True)
        actions = StaffAction.objects.filter(id__in=action_ids)
    
    if not actions.exists():
        actions = StaffAction.objects.all()
    
    return render(request, 'staff/home.html', {'actions': actions})


@cache_control(no_cache=True, must_revalidate=True)
def staff_login(request):
    if 'staff_id' in request.session:
        return redirect('staff_home')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            staff = Staff.objects.get(email=email)
        except Staff.DoesNotExist:
            return render(request, 'staff/staff_login.html', {'msg': 'Invalid Email or Password'})
        

        if not check_password(password, staff.password):
            return render(request, 'staff/staff_login.html', {'msg': 'Invalid Email or Password'})
        
        request.session['staff_id'] = staff.id
        return redirect('staff_home')
    
    return render(request, 'staff/staff_login.html')

def logout(request):
    if 'staff_id' in request.session:
        request.session.flush()
    return redirect('staff_login')
'''___________________________________STAFF_DOCTOR________________________________________________'''


def staff_doctor_list(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login') 
    doctors = Doctor.objects.all()
    doc_name = request.GET.get('doc_name')
    if doc_name:
        doctors = doctors.filter(firstname__icontains=doc_name)
        
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'staff/doctor_list.html', {'doctors':doctors, 'page_obj':page_obj})


# class StaffDoctorListView(ListView):
#     model = Doctor
#     template_name = 'staff/doctor_list.html'
#     context_object_name = 'doctors'
#     paginate_by = 10

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         doc_name = self.request.GET.get('doc_name')
#         if doc_name:
#             queryset = queryset.filter(firstname__icontains=doc_name)
#         return queryset

#     def dispatch(self, request, *args, **kwargs):
#         if 'staff_id' not in request.session:
#             return redirect('staff_login')
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = Paginator(self.get_queryset(), self.paginate_by)
#         page_number = self.request.GET.get('page')
#         context['page_obj'] = paginator.get_page(page_number)
#         return context

'''___________________________________STAFF_PATIENT________________________________________________'''

# def staff_patient_create(request):
#     if 'staff_id' not in request.session:
#         return redirect('staff_login')
#     if request.method =='POST':
#         form = CustomPatientCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('staff_patient_list')
#     else:
#         form = CustomPatientCreationForm()
#     return render(request,'staff/patient_create.html', {'form':form})

class StaffPatientCreateView(CreateView):
    model = Patient
    form_class = CustomPatientCreationForm
    template_name = 'staff/patient_create.html'
    success_url = reverse_lazy('staff_patient_list')
    def dispatch(self, request, *args, **kwargs):
        if 'staff_id' not in request.session:
            return redirect('staff_login')
        return super().dispatch(request, *args, **kwargs)

def staff_patient_list(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    patient = Patient.objects.filter(is_discharged=False)
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
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('staff_patient_list')

def staff_patient_edit(request, patient_id):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == "POST":
        form = CustomPatientModification(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('staff_patient_list')
    else:
        form = CustomPatientModification(instance=patient)
    
    return render(request, 'staff/patient_edit.html', {'form': form, 'patient':patient})

def is_discharged(patient_id=None):
    patient = Patient.objects.get(id=patient_id,is_discharged=True)
    if patient:
        return True
    return False
'''______________________________________PRESCRIPTION____________________________________________'''

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
    


'''______________________________________DISCHARGE____________________________________________'''

def staff_discharge(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    if request.method == 'POST':
        form = DischargeForm(request.POST)
        if form.is_valid():
            patient_id = form.cleaned_data.get('id').id
            patient = get_object_or_404(Patient, id=patient_id)
            if patient.is_discharged:
                return render(request, 'staff/discharge.html', {
                    'msg': "The requested patient already discharged!", 
                    'form': form
                    })
            patient = Patient.objects.get(id=patient_id)
            if not patient:
                msg = "The requested patient does not exist!"
                return render(request, 'staff/discharge.html', {'msg': msg, 'form': form})

            bills = PatientBills.objects.filter(patient=patient, is_completed=False).first()
            if bills:
                msg = "The Patient Bill is NOT PAID!!"
                return render(request, 'staff/discharge.html', {'msg': msg, 'form': form})
            room = patient.room
            if room:
                room.is_vacant = True
                room.save()
            patient.room = None
            patient.is_discharged = True
            patient.checkout_date=date.today()
            patient.save()
            msg = 'Patient Successfully Discharged'
            return render(request, 'staff/discharge.html', {'msg': msg, 'form': form})
    else:
        form = DischargeForm()

    return render(request, 'staff/discharge.html', {'form': form})

'''_______________________________________LAB_REPORT_PDF________________________________________________'''


def generate_pdf_lab_report(request, report_id):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    lab_report = get_object_or_404(LabReport, id=report_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="lab_report_{report_id}.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, f"Lab Report ID: {lab_report.id}")
    p.drawString(100, 780, f"Patient: {lab_report.patient}")
    p.drawString(100, 760, f"Doctor: {lab_report.doctor}")
    p.drawString(100, 740, f"Result: {lab_report.result}")
    p.drawString(100, 720, f"Amount: {lab_report.amount}")
    
    if lab_report.sugar_test:
        p.drawString(100, 700, f"Sugar Test: {lab_report.sugar_test}")
    if lab_report.liver_test:
        p.drawString(100, 680, f"Liver Function Test: {lab_report.liver_test}")
    if lab_report.cholesterol_test:
        p.drawString(100, 660, f"Cholesterol Test: {lab_report.cholesterol_test}")
    if lab_report.kidney_test:
        p.drawString(100, 640, f"Kidney Function Test: {lab_report.kidney_test}")

    p.showPage()
    p.save()
    
    return response

def save_pdf_lab_report(lab_report):
    
    report_id = lab_report.id
    file_path = os.path.join('docs', f'lab_report_{report_id}.pdf')

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    p = canvas.Canvas(file_path)

    p.drawString(100, 800, f"Lab Report ID: {lab_report.id}")
    p.drawString(100, 780, f"Patient: {lab_report.patient}")
    p.drawString(100, 760, f"Doctor: {lab_report.doctor}")
    p.drawString(100, 740, f"Result: {lab_report.result}")
    p.drawString(100, 720, f"Amount: {lab_report.amount}")

    if lab_report.sugar_test:
        p.drawString(100, 700, f"Sugar Test: {lab_report.sugar_test}")
    if lab_report.liver_test:
        p.drawString(100, 680, f"Liver Function Test: {lab_report.liver_test}")
    if lab_report.cholesterol_test:
        p.drawString(100, 660, f"Cholesterol Test: {lab_report.cholesterol_test}")
    if lab_report.kidney_test:
        p.drawString(100, 640, f"Kidney Function Test: {lab_report.kidney_test}")

    p.showPage()
    p.save()

    return file_path

def send_lab_report_email(patient_email, pdf_path):
    subject = 'Your Lab Report'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [patient_email]

    email = EmailMessage(
        subject=subject,
        body='Please find attached your lab report.',
        from_email=email_from,
        to=recipient_list,
    )
    try:
        with open(pdf_path, 'rb') as f:
            email.attach(os.path.basename(pdf_path), f.read(), 'application/pdf')
    except Exception as e:
        print(f"Error attaching file: {e}")
        return

    try:
        email.send()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
        

def staff_labreport_create(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    if request.method == 'POST':
        form = LabReportCreation(request.POST)
        
        if form.is_valid():
            patient = form.cleaned_data.get('patient')
            patient_id = patient.id
            doctor = form.cleaned_data.get('doctor')
            result = form.cleaned_data.get('result')

            lab_report = LabReport.objects.create(
                patient=patient,
                doctor=doctor,
                result=result
            )
            amount = 0
            st = SugarTest.objects.filter(patient=patient_id, is_completed=False).first()
            if st is not None:
                lab_report.sugar_test = st
                amount += st.price
            
            lt = LiverFunctionTest.objects.filter(patient=patient_id, is_completed=False).first()
            if lt is not None:
                lab_report.liver_test = lt
                amount += lt.price
            
            ct = CholesterolTest.objects.filter(patient=patient_id, is_completed=False).first()
            if ct is not None:
                lab_report.cholesterol_test = ct
                amount += ct.price
            
            kt = KidneyFunctionTest.objects.filter(patient=patient_id, is_completed=False).first()
            if kt is not None:
                lab_report.kidney_test = kt
                amount += kt.price
            
            lab_report.amount = amount
            lab_report.save()

            try:
                BASE_DIR = settings.BASE_DIR
                
                pdf_filename = f'lab_report_{lab_report.id}.pdf'
                pdf_path = os.path.join(BASE_DIR, 'docs', pdf_filename)
                print('@@@@@@@@@@@@@@@',pdf_path)
                patient_email = patient.email
                save_pdf_lab_report(lab_report)
                send_lab_report_email(patient_email, pdf_path)
                
            except Exception as e:
                print(f"Error: {e}")

            return redirect('staff_home')
    else:
        form = LabReportCreation()
    
    return render(request, 'staff/lab_report_create.html', {'form': form})

def staff_lab_report(request, liver_test_id=None, kidney_test_id=None, sugar_test_id=None, cholesterol_test_id=None):
    if request.method == 'POST':
        form = LabReportCreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_home') 
    else:
        form = LabReportCreation()
    return render(request, 'staff/lab_report.html',{'form':form})

'''______________________________________TESTS____________________________________________'''


def create_kidney_test(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    if request.method == 'POST':
        form = KidneyTestForm(request.POST)
        patient_id = request.POST.get('patient')

        if form.is_valid():
            patient = get_object_or_404(Patient, id=patient_id)
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
            
            concatenated_values = f"{urea_value}, {creatinine_value}, {uric_acid_value}, {calcium_total_value}, {phosphorus_value}, {alkaline_phosphatase_value}, {total_protein_value}, {albumin_value}, {sodium_value}, {potassium_value}, {chloride_value}"
            new_kidney_test = KidneyFunctionTest.objects.create(
                patient=patient,
                result=concatenated_values,
            )
            new_kidney_test.save()
            bills = PatientBills.objects.filter(patient_id=patient_id, is_completed=False).first()
            if bills:
                bills.lab_report_bill += 935
                bills.save()
            else:
                PatientBills.objects.create(patient_id=patient_id,lab_report_bill= 935)
            return redirect('test')
        else:

            error_message = 'Please select a patient and fill all required fields.' if not patient_id else 'Please fill all required fields.'
            patients = Patient.objects.all()
            kft = KFT.objects.all()
            return render(request, 'staff/kidney_test.html', {'form': form, 'kft': kft, 'patients': patients, 'error': error_message})
    else:
        form = KidneyTestForm()
        kft = KFT.objects.all()
        patients = Patient.objects.all()
        return render(request, 'staff/kidney_test.html', {'form': form, 'kft': kft, 'patients': patients})


def create_cholesterol_test(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    if request.method == 'POST':
        form = CholesterolTestForm(request.POST)
        patient_id = request.POST.get('patient')
        if form.is_valid() and patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            total_cholesterol = form.cleaned_data.get('total_cholesterol')
            ldl_cholesterol = form.cleaned_data.get('ldl_cholesterol')
            hdl_cholesterol = form.cleaned_data.get('hdl_cholesterol')
            triglycerides = form.cleaned_data.get('triglycerides')
            concatenated_values = f'{total_cholesterol}, {ldl_cholesterol}, {hdl_cholesterol}, {triglycerides}'
            new_cholesterol_test = CholesterolTest.objects.create(
                result=concatenated_values,
                patient=patient,
            )
            new_cholesterol_test.save()
            bills = PatientBills.objects.filter(patient_id=patient_id, is_completed=False).first()
            if bills:
                bills.lab_report_bill += 450
                bills.save()
            else:
                PatientBills.objects.create(patient_id=patient_id,lab_report_bill= 450)
            return redirect('test')
        else:
            error_message = 'Please select a patient and fill all required fields.' if not patient_id else 'Please fill all required fields.'
            patients = Patient.objects.all()
            ct = CT.objects.all()
            return render(request, 'staff/cholesterol_test.html', {'form': form, 'ct': ct, 'patients': patients, 'error': error_message})
    else:
        form = CholesterolTestForm()
        ct = CT.objects.all()
        patients = Patient.objects.all()
        return render(request, 'staff/cholesterol_test.html', {'form': form, 'ct': ct, 'patients': patients})


def create_sugar_test(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    if request.method == 'POST':
        form = SugarTestForm(request.POST)
        patient_id = request.POST.get('patient')
        if form.is_valid() and patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            fbs_value = form.cleaned_data.get('fbs')
            pbs_value = form.cleaned_data.get('pbs')
            rbs_value = form.cleaned_data.get('rbs')
            hba1c_value = form.cleaned_data.get('hba1c')
            ogtt_value = form.cleaned_data.get('ogtt')
            concatenated_values = f'{fbs_value}, {pbs_value}, {rbs_value}, {hba1c_value}, {ogtt_value}'
            new_sugar_test = SugarTest.objects.create(
                patient=patient,
                result=concatenated_values,
            )
            new_sugar_test.save()
            bills = PatientBills.objects.filter(patient_id=patient_id, is_completed=False).first()
            if bills:
                bills.lab_report_bill += 175
                bills.save()
            else:
                PatientBills.objects.create(patient_id=patient_id,lab_report_bill= 175)
            return redirect('test')
        else:
            error_message = 'Please select a patient and fill all required fields.' if not patient_id else 'Please fill all required fields.'
            st = ST.objects.all()
            patients = Patient.objects.all()
            return render(request, 'staff/sugar_test.html', {'form': form, 'st': st, 'patients': patients, 'error': error_message})
    else:
        form = SugarTestForm()
        st = ST.objects.all()
        patients = Patient.objects.all()
        return render(request, 'staff/sugar_test.html', {'form': form, 'st': st, 'patients': patients})

def create_liver_test(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')
    if request.method == 'POST':
        form = LiverTestForm(request.POST)
        patient_id = request.POST.get('patient')
        if form.is_valid() and patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            total_bilirubin = form.cleaned_data.get('total_bilirubin')
            direct_bilirubin = form.cleaned_data.get('direct_bilirubin')
            indirect_bilirubin = form.cleaned_data.get('indirect_bilirubin')
            ast_sgot = form.cleaned_data.get('ast_sgot')
            alt_sgot = form.cleaned_data.get('alt_sgpt')
            alp = form.cleaned_data.get('alp')
            total_protein = form.cleaned_data.get('total_protein')
            albumin = form.cleaned_data.get('albumin')
            globulin = form.cleaned_data.get('globulin')
            albumin_globulin_ratio = form.cleaned_data.get('albumin_globulin_ratio')
            concatenated_values = f'{total_bilirubin}, {direct_bilirubin}, {indirect_bilirubin}, {ast_sgot}, {alt_sgot}, {alp}, {total_protein}, {albumin}, {globulin}, {albumin_globulin_ratio}'
            new_lft = LiverFunctionTest.objects.create(
                result=concatenated_values,
                patient=patient,
            )
            new_lft.save()
            bills = PatientBills.objects.filter(patient_id=patient_id, is_completed=False).first()
            if bills:
                bills.lab_report_bill += 670
                bills.save()
            else:
                PatientBills.objects.create(patient_id=patient_id,lab_report_bill= 670)
                
            return redirect('test')
        else:
            error_message = 'Please select a patient and fill all required fields.' if not patient_id else 'Please fill all required fields.'
            lft = LFT.objects.all()
            patients = Patient.objects.all()
            return render(request, 'staff/liver_test.html', {'form': form, 'lft': lft, 'patients': patients, 'error': error_message})
    else:
        form = LiverTestForm()
        lft = LFT.objects.all()
        patients = Patient.objects.all()
        return render(request, 'staff/liver_test.html', {'form': form, 'lft': lft, 'patients': patients})    


'''______________________________________ROOMS____________________________________________'''


def staff_rooms(request):
    
    if request.method == "GET":
        room_no = request.GET.get('search')
        rooms = Room.objects.filter(room_number__icontains=room_no) if room_no else Room.objects.all()
        context = {'rooms': rooms, 'room_no': room_no}
        return render(request, 'staff/rooms.html', context)
@cache_control(no_store=True)
def create_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_rooms')
    else:
        form = CreateRoomForm()
    return render(request, 'staff/create_rooms.html', {'form': form})

@cache_control(no_store=True)
def assign_patient(request,room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method=="POST":
        patient_id = request.POST.get('patient_id')
        if not room.is_vacant:
            error_message = "This room is already occupied."
            return render(request, 'staff/assign_patient.html', {'message': error_message, 'room_id': room_id})
        
        patient = Patient.objects.get(id=patient_id)
        patient.room=room
        patient.save()
        room_update = Room.objects.filter(id=room_id).update(is_vacant=False)
        bills = PatientBills.objects.filter(patient_id=patient_id, is_completed=False).first()
        if bills:
            bills.room = room
            bills.save()
        else:
            PatientBills.objects.create(patient_id=patient_id,room=room)
        if  room_update:
            return redirect('staff_rooms')
        else:
            error_message = "Patient or Room does not exists"
        return render(request, 'staff/assign_patient.html', {'message': error_message, 'room_id': room_id})
    return render(request, 'staff/assign_patient.html', {'room_id': room_id})
    
'''______________________________________MEDICINE____________________________________________'''

def create_medicine_list(request):
    medicines = Medicine.objects.all()
    if request.method == 'POST':
        form = MedicineBillCreationForm(request.POST)
        
        if form.is_valid():
            patient = form.cleaned_data.get('patient')
           
            if patient is None:
                return render(request, 'staff/create_medicine_list.html', {
                    'medicines': medicines,
                    'form': form,
                    'msg':'Invalid Patient ID'
                })
            patient_id = patient.id
            total_price = request.POST.get('total_price')
            bills = PatientBills.objects.filter(patient_id=patient_id, is_completed=False)
            
            if bills.exists():
                bill = bills.first()
                bill.medicine_bill += float(total_price)
                bill.save()
            else:
                PatientBills.objects.create(patient_id=patient_id,medicine_bill = float(total_price))
            
            return render(request, 'staff/create_medicine_list.html', {
                    'medicines': medicines,
                    'form': form,
                    'msg':'Medicine Bill Successfully Generated'
                })
    else:
        form = MedicineBillCreationForm()
    
    return render(request, 'staff/create_medicine_list.html', {
        'medicines': medicines,
        'form': form
    })
    


'''______________________________________APPOINTMENT____________________________________________'''


# def staff_appointment(request):
#     if request.method == 'POST':
#         form = AppointmentCreationForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
            
#             patient = form.cleaned_data.get('patient')
#             doctor = form.cleaned_data.get('doctor')
#             patient_id = patient.pk
#             doctor_id = doctor.pk
#             appointment.patient_id = patient_id
#             appointment.doctor_id = doctor_id
#             appointment.appointment_id = generate_random_string()
            
#             appointment.save()
            
#             messages.success(request, "Appointment created successfully!")
#             return redirect('staff_home')  
#     else:    
#         form = AppointmentCreationForm()
    
#     return render(request, 'staff/appointment.html', {'form': form})



'''______________________________________AVAILABILITY____________________________________________'''

def create_availability(request):
    if request.method == 'POST':
        form = DoctorAvailabilityCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('staff_doctor_list')
    else:
        form = DoctorAvailabilityCreationForm()
        
    return render(request, 'staff/create_availability.html', {'form': form})


def appointment(request, doctor_id, date):
    if request.method == 'GET':
        print(doctor_id, date)
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availability = DoctorAvailability.objects.filter(doctor=doctor, date=date, is_available=True)
    
    # if not availability.exists():

    #     return render(request, 'staff/select_doctor.html')
    
    if request.method == 'POST':
        timeslot = request.POST.get('timeslot')
        patient_id = request.POST.get('patient_id')
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
                return redirect('staff_home')
            except DoctorAvailability.DoesNotExist:
                messages.error(request, "The selected time slot is not available.")
        else:
            messages.error(request, "Please provide all the required details.")
    else:
        messages.error(request, "Invalid request method.")
    
    return render(request, 'staff/doctor_availability.html', {
        'doctor': doctor,
        'date': date,
        'availability': availability
    })
    
def select_date(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availability = DoctorAvailability.objects.filter(doctor=doctor).values('date', 'timeslot')

    available_dates = list(availability.values_list('date', flat=True).distinct())
    available_dates_json = json.dumps([str(date) for date in available_dates])
    return render(request, 'staff/select_date.html', {'doctor': doctor, 'available_dates_json': available_dates_json})
    

def select_doctor(request):
    if request.method=='POST':
        doctor = Doctor.objects.all()
        
    doctor = Doctor.objects.all()
    return render(request, 'staff/select_doctor.html', {'doctor':doctor})
'''______________________________________INVOICE____________________________________________'''
def invoice_list(request):
    if request.method == 'GET':
        invoices = Invoice.objects.all().order_by('id')
        patient_name = request.GET.get('patient_name', '')

        if patient_name:
            invoices = invoices.filter(patient_id__firstname__icontains=patient_name) | invoices.filter(patient_id__lastname__icontains=patient_name)

        paginator = Paginator(invoices, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, 'staff/invoice_list.html', {'page_obj': page_obj})

    

def staff_invoice(request):
    tax_rate = 0.05    # 5%
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)  
            patient = invoice.patient_id
            patient_id = patient.id
            old_invoice = Invoice.objects.filter(patient_id=invoice.patient_id, status='pending').first()
            if old_invoice:
                msg = 'Invoice already Created'
                invoice_id = old_invoice.id
                return render(request, 'staff/invoice.html', {'msg':msg, 'invoice_id':invoice_id} )
            
            bills = PatientBills.objects.filter(patient_id=patient_id, is_completed=False).first()

            if not bills:
                return render(request, 'staff/invoice.html', {'form': form, 'error_msg': 'No Bill Exist'})
            if patient.room_id:
                today = date.today()
                duration = (today - patient.admission_date).days 
                if duration == 0:
                    duration = 1
                invoice.room_charges = duration * patient.room.price
            else:
                invoice.room_charges = 0
            invoice.total_amount = invoice.room_charges
            
            invoice.bill_id = bills
            invoice.total_amount += (bills.medicine_bill or 0) + (bills.lab_report_bill or 0)

            tax = invoice.total_amount + tax_rate
            invoice.total_amount += tax
            invoice.invoice_no = generate_random_string()
            invoice.date = date.today()

            invoice.save()  
            url = reverse('amount_conformation', args=[invoice.id])
            return redirect(url)
    else:
        form = InvoiceForm()
    return render(request, 'staff/invoice.html', {'form': form})

def invoice_delete(request, invoice_id):
    invoice =get_object_or_404(Invoice,id=invoice_id)
    invoice.delete()
    return redirect('invoice_list')  

def test(request):
    kidney_test = KidneyFunctionTest.objects.all()
    
    return render(request, 'staff/tests.html',{'kidney_test':kidney_test})


'''______________________________________PAYMENT____________________________________________'''


def amount_conformation(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    payment_completed = invoice.status == "Success" or invoice.total_amount <= 0

    if payment_completed:
        messages = 'Bill Already Paid or Invalid Amount'
    else:
        messages = 'Proceed to Payment'
        
    context = {
        'payment_status':invoice.status,
        'invoice': invoice,
        'room': invoice.room_charges if invoice.room_charges > 0 else None,
        'lab_report': invoice.bill_id.lab_report_bill if invoice.bill_id and invoice.bill_id.lab_report_bill > 0 else None,
        'medicine': invoice.bill_id.medicine_bill if invoice.bill_id and invoice.bill_id.medicine_bill > 0 else None,
        'amount': invoice.total_amount if invoice.total_amount > 0 else None,
        'invoice_id': invoice_id,
        'payment_method':invoice.payment_method,
        'messages': messages,
        'payment_completed':payment_completed
    }
    return render(request, 'staff/amount_conformation.html', context)


'''<----------------------------------------------RAZORPAY----------------------------------------------->'''


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET ))

def create_order(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    total_amount = int(invoice.total_amount * 100)
    DATA = {
        'amount':total_amount,
        'currency':'INR',
        'payment_capture':1
    }
    order = razorpay_client.order.create(data=DATA)
    order_id =order['id']
    context = {
        'order_id': order_id,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'invoice': invoice
    }
    
    return render(request,'staff/razorpay.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        invoice_id = request.POST.get('invoice_id')

        payment_details_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(payment_details_dict)
        except razorpay.errors.SignatureVerificationError:

            messages.error(request, "Payment verification failed. Please try again.")
            return redirect('staff_home')
        invoice = get_object_or_404(Invoice, id=invoice_id)
        invoice.status = 'Success'
        patient=invoice.patient_id
        patient_bill = PatientBills.objects.get(patient=patient,is_completed=False)
        patient_bill.is_completed = True
        patient_bill.save()
        invoice.save()

        return render(request, 'staff/payment_success.html', {'invoice': invoice})

    return redirect('staff_home')

'''<----------------------------------------------PAYPAL----------------------------------------------->'''


INR_TO_USD_RATE = Decimal('0.012')

def create_paypal_payment(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    total_amount_usd = round(invoice.total_amount * INR_TO_USD_RATE, 2)
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_paypal_payment', args=[invoice_id])),
            "cancel_url": request.build_absolute_uri(reverse('payment_paypal_cancelled'))
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": f"Invoice {invoice.invoice_no}",
                    "sku": f"INV-{invoice_id}",
                    "price": str(total_amount_usd),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(total_amount_usd),
                "currency": "USD"
            },
            "description": f"Payment for Invoice {invoice.invoice_no}"
        }]
    })
    
    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        print(payment.error)
        error_details = payment.error.get('details', []) if payment.error else []
        return render(request, 'staff/payment_paypal_error.html', {
            'error': payment.error,
            'error_details': error_details
        })

def execute_paypal_payment(request, invoice_id):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.status = "Success"
        invoice.save()
        return redirect('payment_paypal_success')
    else:
        return render(request, 'staff/payment_paypal_error.html', {'error': payment.error})

def payment_paypal_success(request):
    return render(request, 'staff/payment_paypal_success.html')

def payment_paypal_cancelled(request):
    return render(request, 'staff/payment_paypal_cancelled.html')

'''_______________________________________OTP_SENDING_____________________________________________'''

def send_otp_email(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            otp = generate_otp()
        
            user_otp = UserOTP(email=email, otp=otp)
            user_otp.save()
            subject = 'Your Lab Report'
            message = f'Please find attached your lab report.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('validate_otp') 
    else:
        form = OTPForm()
    return render(request, 'staff/send_otp.html', {'form': form})

def validate_otp(request):
    if request.method == 'POST':
        form = OTPValidationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            otp = form.cleaned_data.get('otp')

            valid_time = timezone.now() - timedelta(minutes=10) 
            user_otp = UserOTP.objects.filter(email=email, otp=otp, created_at__gte=valid_time).first()
            
            if user_otp:
                return HttpResponse('OTP is valid')
            else:
                return HttpResponse('Invalid OTP or OTP has expired')
    else:
        form = OTPValidationForm()
    
    return render(request, 'staff/validate_otp.html', {'form': form})











# https://www.dbdiagram.io/d/Hospital-Management-665befbcb65d933879443c64