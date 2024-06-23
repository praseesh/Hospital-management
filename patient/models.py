from django.db import models
from datetime import datetime

class Room(models.Model):
    ROOM_TYPES = [
        ('General', 'General'),
        ('ICU', 'ICU'),
        ('Rooms', 'Rooms'),
    ]
    
    room_number = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, choices=ROOM_TYPES)
    is_vacant = models.BooleanField(default=True)
    price = models.IntegerField()

    class Meta:
        db_table = 'rooms'
        
    def is_vacant(self):
        return not self.patient_set.exists()
    
    def __str__(self):
        return f"{self.room_number} - {self.type}"

class Patient(models.Model):
    firstname = models.CharField(max_length=255, blank=False, null=False)
    lastname = models.CharField(max_length=255, blank=True, null=True)  
    mobile = models.CharField(max_length=20, unique=True, blank=False, null=False)
    email = models.CharField(max_length=255, unique=True, blank=False, null=False)
    dob = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=7, blank=True, null=True) 
    address = models.CharField(max_length=255, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateField(blank=True, null=True)
    checkout_date = models.DateField(blank=True, null=True, default=None) 
    
    class Meta:
        db_table = 'patient'     

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
