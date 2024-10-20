from django.urls import path
from . import views
from .views import StaffPatientCreateView

urlpatterns = [
    path('', views.staff, name='staff_home'),
    path('login', views.staff_login, name="staff_login"),
    path('logout',views.logout,name="staff_logout"),
    path('staff_details_edit/<int:staff_id>/', views.staff_details_edit, name='staff_details_edit'),
    path('doctors/', views.staff_doctor_list, name='staff_doctor_list'),
    path('patient', views.staff_patient_list, name='staff_patient_list'),
    path('patient/<int:patient_id>', views.staff_patient_details, name='staff_patient_details'),
    path('staff/patient/create/', StaffPatientCreateView.as_view(), name='staff_patient_create'),
    path('patient/edit/<int:patient_id>', views.staff_patient_edit, name='staff_patient_edit'),
    path('patient/delete/<int:patient_id>', views.staff_patient_delete, name='staff_patient_delete'),
    
    path('invoice_list', views.invoice_list, name='invoice_list'),
    path('invoice/',views.staff_invoice,name="staff_invoice"),
    path('invoice/delete/<int:invoice_id>', views.invoice_delete, name='invoice_delete'),
    
    path('amount_conformation/<int:invoice_id>', views.amount_conformation, name='amount_conformation'),
    path('create_order/<int:invoice_id>/', views.create_order, name='create_order'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('create_paypal_payment/<int:invoice_id>/', views.create_paypal_payment, name='create_paypal_payment'),
    path('execute_paypal_payment/<int:invoice_id>/', views.execute_paypal_payment, name='execute_paypal_payment'),
    path('payment_paypal_success/', views.payment_paypal_success, name='payment_paypal_success'),
    path('payment_paypal_cancelled/', views.payment_paypal_cancelled, name='payment_paypal_cancelled'),
    
    path('lab_report', views.staff_lab_report, name="staff_lab_report"),
    path('lab_report_create/', views.staff_labreport_create, name='lab_report_create'),
    path('kidney_test',views.create_kidney_test,name="create_kidney_test"),
    path('sugar_test',views.create_sugar_test,name="create_sugar_test"),
    path('liver_test',views.create_liver_test,name="create_liver_test"),
    path('cholesterol_test', views.create_cholesterol_test, name="create_cholesterol_test"),
    
    path('prescription', views.staff_prescription, name="staff_prescription"),
    path('prescription/delete/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),
    path('prescription_create', views.staff_prescription_create, name="staff_prescription_create"),
    path('staff_prescription_list', views.staff_prescription, name="staff_prescription_list"),
    path('staff_appointment', views.staff_appointment,name="staff_appointment"),
    
    path('discharge', views.staff_discharge, name="staff_discharge"),
    
    path('staff_rooms', views.staff_rooms, name="staff_rooms"),
    path('create_room',views.create_room, name="create_room"),
    path('room_search', views.staff_rooms,name="room_search"),
    path('assign_patient/<int:room_id>/', views.assign_patient, name='assign_patient'),
    
    path('create_medicine_list', views.create_medicine_list, name="create_medicine_list"), 
    path('test',views.test, name="test"),
    
    path('send-otp/', views.send_otp_email, name='send_otp'),
    path('validate-otp/', views.validate_otp, name='validate_otp'),
    
    path('create_availability', views.create_availability, name="create_availability"),
    path('select_date/<int:doctor_id>/', views.select_date, name='select_date'),
    path('appointment/<int:doctor_id>/<str:date>/', views.appointment, name='doctor_availability'),
    path('select_doctor', views.select_doctor,name="select_doctor")
]