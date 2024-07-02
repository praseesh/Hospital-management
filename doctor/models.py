from django.db import models


class DoctorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Doctor(models.Model):
    firstname = models.CharField(max_length=255, blank=False, null=False)
    lastname = models.CharField(max_length=255, blank=True, null=True)  
    specialty = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    availability = models.CharField(max_length=255, blank=True, null=True)  
    contact = models.CharField(max_length=255, blank=True, null=True)  
    password = models.CharField(max_length=255, blank=False, null=False, default=1234)
    is_deleted = models.BooleanField(default=False)
    
    objects = DoctorManager()
    
    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
        
    def delete(self):
        self.is_deleted = True
        self.save()




