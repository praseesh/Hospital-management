from django.db import models
from doctor.models import Doctor
from patient.models import Patient

class StaffManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class DeletedStaffManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)
    
class Roles(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'roles'
    
    def __str__(self):
        return self.name

class Staff(models.Model):
    firstname = models.CharField(max_length=255, blank=False, null=False,default='')
    lastname = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, default=1)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=255, blank=False, null=True, unique=True)
    password = models.CharField(max_length=255, blank=False, null=False, default=1234)
    is_deleted = models.BooleanField(default=False)

    objects = StaffManager() 
    all_objects = AllObjectsManager()  
    deleted_objects = DeletedStaffManager()  

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def delete(self):
        self.is_deleted = True
        self.save()
    
class StaffAction(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=255)
    url_name = models.CharField(max_length=100, default="")

    class Meta:
        db_table = 'staff_action'

    def __str__(self):
        return f"{self.name} {self.role} {self.description} {self.url_name}"
    


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    instructions = models.TextField(blank=True)
    date_issued = models.DateField()
    created_by = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified_by = models.IntegerField()
    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prescriptions'
        
    
