from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff, name='staff_home'),
    path('login', views.staff_login, name="staff_login")
]