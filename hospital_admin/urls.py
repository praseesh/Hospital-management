from django.urls import path
from . import views

urlpatterns = [
    path('login', views.admin_login, name='login'),
    path('', views.home, name='admin_home'),
    path('logout',views.logout, name='logout'),
    
    path('staff', views.staff_list, name='staff_list'),
    path('staff.create', views.staff_create, name='staff_create'),
    path('staff/<int:staff_id>', views.staff_details, name='staff_detail'),
    path('staff/edit/<int:staff_id>', views.staff_edit, name='staff_edit'),
    path('staff/delete/<int:staff_id>', views.staff_delete, name='staff_delete'),
    path('deleted-staff/', views.deleted_staff_list, name='deleted_staff_list'),
    
    path('doctors', views.doctor_list, name='doctor_list'),
    path('doctor/create', views.doctor_create, name='doctor_create'),
    path('doctors/<int:doctor_id>', views.doctor_detail, name='doctor_detail'),
    path('doctors/edit/<int:doctor_id>', views.doctor_edit, name='doctor_edit'),
    path('doctor/delete/<int:doctor_id>', views.doctor_delete, name="doctor_delete"),
    
    path('patient', views.patient_list, name='patient_list'),
    path('patient/<int:patient_id>', views.patient_details, name='patient_detail'),
    path('patient/create', views.patient_create, name='patient_create'),
    path('patient/edit/<int:patient_id>', views.patient_edit, name='patient_edit'),
    path('patient/delete/<int:patient_id>', views.patient_delete, name="patient_delete")

]