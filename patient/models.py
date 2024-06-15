from django.db import models
from datetime import datetime

class Patient(models.Model):
    firstname = models.CharField(max_length=255, blank=False, null=False)
    lastname = models.CharField(max_length=255, blank=True, null=True)  
    mobile = models.CharField(max_length=20, unique=True, blank=False, null=False)
    email = models.CharField(max_length=255, unique=True, blank=False, null=False)
    dob = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=7, blank=True, null=True) 
    address = models.CharField(max_length=255, blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True, default=datetime.now)
    checkout_date = models.DateField(blank=True, null=True, default=None) 
    
    class Meta:
        db_table = 'patient'     

    def __str__(self):
        return f"{self.firstname} {self.lastname}"