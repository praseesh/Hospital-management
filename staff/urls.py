from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff, name='staff_home'),
    path('login', views.staff_login, name="staff_login"),
    path('doctors/', views.staff_doctor_list, name='staff_doctor_list'),
    
    # path('patients/', views.staff_patient_list, name='staff_patient_list'),
    path('patient', views.staff_patient_list, name='staff_patient_list'),
    path('patient/<int:patient_id>', views.staff_patient_details, name='staff_patient_details'),
    path('patient/create', views.staff_patient_create, name='staff_patient_create'),
    path('patient/edit/<int:patient_id>', views.staff_patient_edit, name='staff_patient_edit'),
    path('patient/delete/<int:patient_id>', views.staff_patient_delete, name='staff_patient_delete'),
    
    path('invoice',views.staff_invoice,name='staff_invoice'),
    path('lab_report', views.staff_lab_report, name="staff_lab_report"),
    path('prescription', views.staff_prescription, name="staff_prescription"),
    path('discharge', views.staff_discharge, name="staff_discharge"),
    path('rooms', views.staff_rooms, name="staff_rooms"),
    path('appointment', views.staff_appointment, name="staff_appointment"),
    path('patient/edit/<int:patient_id>', views.staff_patient_edit, name="staff_patient_edit"),
    
]