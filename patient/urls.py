from django.urls import path
from .import views
urlpatterns = [

    path('',views.home,name='home'),
    path('select_doctor',views.select_doctor,name="select_doctor"),
    path('select_date/<int:doctor_id>/',views.select_date, name="select_date"),
    path('appointment/<int:doctor_id>/<str:date>/', views.appointment, name="appointment"),
    path('patient_create', views.patient_create, name="patient_add"),
    path('patient_registration',views.patient_registration,name="patient_registration"),
]