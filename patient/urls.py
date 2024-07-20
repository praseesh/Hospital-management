from django.urls import path
from .import views
urlpatterns = [

    path('',views.home,name='home'),
    path('select_doctor/<int:patient_id>/', views.select_doctor, name='select_doctor'),
    path('select_date/<int:patient_id>/<int:doctor_id>/', views.select_date, name='select_date'),
    path('appointment/<int:patient_id>/<int:doctor_id>/<str:date>/', views.appointment, name="appointment"),
    path('patient_create', views.patient_create, name="patient_add"),
    path('patient_selection',views.patient_selection,name="patient_selection"),
]