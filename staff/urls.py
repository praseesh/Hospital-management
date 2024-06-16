from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff, name='staff_home'),
    path('login', views.staff_login, name="staff_login"),
    path('doctors/', views.staff_doctor_list, name='staff_doctor_list'),
    path('patients/', views.staff_patient_list, name='staff_patient_list'),
    path('invoice',views.staff_invoice,name='staff_invoice'),
    path('lab_report', views.staff_lab_report, name="staff_lab_report"),
    path('prescription', views.staff_prescription, name="staff_prescription"),
    path('discharge', views.staff_discharge, name="staff_discharge"),
    path('rooms', views.staff_rooms, name="staff_rooms"),
    path('appointment', views.staff_appointment, name="staff_appointment"),
]