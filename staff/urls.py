from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff, name='staff_home'),
    path('login', views.staff_login, name="staff_login"),
    path('doctors/', views.staff_doctor_list, name='staff_doctor_list'),
    
    path('patient', views.staff_patient_list, name='staff_patient_list'),
    path('patient/<int:patient_id>', views.staff_patient_details, name='staff_patient_details'),
    path('patient/create', views.staff_patient_create, name='staff_patient_create'),
    path('patient/edit/<int:patient_id>', views.staff_patient_edit, name='staff_patient_edit'),
    path('patient/delete/<int:patient_id>', views.staff_patient_delete, name='staff_patient_delete'),
    
    path('invoice',views.staff_invoice,name='staff_invoice'),
    
    path('lab_report', views.staff_lab_report, name="staff_lab_report"),
    path('lab_report_create',views.staff_labreport_create, name="lab_report_create" ),
    path('kidney_test',views.create_kidney_test,name="create_kidney_test"),
    path('sugar_test',views.create_sugar_test,name="create_sugar_test"),
    path('liver_test',views.create_liver_test,name="create_liver_test"),
    path('cholesterol_test', views.create_cholesterol_test, name="create_cholesterol_test"),
    
    path('prescription', views.staff_prescription, name="staff_prescription"),
    path('prescription/delete/<int:prescription_id>', views.delete_prescription, name='delete_prescription'),
    path('prescription_create', views.staff_prescription_create, name="staff_prescription_create"),
    path('staff_prescription_list', views.staff_prescription, name="staff_prescription_list"),
    
    path('discharge', views.staff_discharge, name="staff_discharge"),
    
    path('create_room',views.create_rooms, name="create_room"),
    path('rooms', views.rooms, name="staff_rooms"),
    path('appointment', views.staff_appointment, name="staff_appointment"),
    path('patient/edit/<int:patient_id>', views.staff_patient_edit, name="staff_patient_edit"),
    
    # path('staff/prescription/send_email/<int:prescription_id>/', views.send_email, name='send_email'),

]