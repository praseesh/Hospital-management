from django.db import models
from datetime import datetime
from doctor.models import Doctor

class Room(models.Model):
    ROOM_TYPES = [
        ('General', 'General'),
        ('ICU', 'ICU'),
        ('Rooms', 'Rooms'),
    ]
    
    room_number = models.CharField(max_length=50, unique=True)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    is_vacant = models.BooleanField(default=True)
    price = models.IntegerField()

    class Meta:
        db_table = 'rooms'
    
    def __str__(self):
        return f"{self.room_number} - {self.type}"

class Patient(models.Model):
    DISEASE_CHOICES = [
        ('fever', 'Fever'),
        ('headache', 'Headache'),
        ('flu', 'Flu'),
        ('covid', 'COVID-19'),
        ('diabetes', 'Diabetes'),
        ('hypertension', 'Hypertension'),
        ('asthma', 'Asthma'),
        ('arthritis', 'Arthritis'),
        ('cancer', 'Cancer'),
        ('depression', 'Depression'),
        ('allergy', 'Allergy'),
        ('pneumonia', 'Pneumonia'),
        ('bronchitis', 'Bronchitis'),
        ('migraine', 'Migraine'),
        ('insomnia', 'Insomnia'),
        ('other', 'Other'),
    ]

    firstname = models.CharField(max_length=255, blank=False, null=False)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=20, unique=True, blank=False, null=False)
    email = models.CharField(max_length=255, unique=True, blank=False, null=False)
    dob = models.DateField(blank=False, null=False)
    disease = models.CharField(max_length=50, choices=DISEASE_CHOICES, blank=False, null=False, default='')
    gender = models.CharField(max_length=7, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateField(blank=True, null=True)
    checkout_date = models.DateField(blank=True, null=True, default=None)

    class Meta:
        db_table = 'patient'     

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    

class Appointment(models.Model):
    APPOINTMENT_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    DISEASE_CHOICES = [
        ('fever', 'Fever'),
        ('headache', 'Headache'),
        ('flu', 'Flu'),
        ('covid', 'COVID-19'),
        ('diabetes', 'Diabetes'),
        ('hypertension', 'Hypertension'),
        ('asthma', 'Asthma'),
        ('arthritis', 'Arthritis'),
        ('cancer', 'Cancer'),
        ('depression', 'Depression'),
        ('allergy', 'Allergy'),
        ('pneumonia', 'Pneumonia'),
        ('bronchitis', 'Bronchitis'),
        ('migraine', 'Migraine'),
        ('insomnia', 'Insomnia'),
        ('other', 'Other'),
    ]

    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False, blank=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=APPOINTMENT_STATUS_CHOICES, default='scheduled')
    reason_for_visit = models.TextField(choices=DISEASE_CHOICES, blank=False, null=False, default='Other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'appointment'

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.patient} with {self.doctor} on {self.appointment_date}"

    
