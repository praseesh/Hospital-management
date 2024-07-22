from django.urls import path
from .import views
urlpatterns = [

    path('',views.home,name='doctor_home'),
    path('appointment',views.doctor_appointment,name='doctor_appointment'),
    path('appointment/<str:date>/',views.view_appointment,name='view_appointment'),
    path('doctor_logout',views.doctor_logout,name="doctor_logout" ),
    path('edit_doctor_profile',views.edit_doctor_profile,name="edit_doctor_profile"),
    path('create_doctor_availability',views.create_doctor_availability,name="create_doctor_availability"),
]