from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class DoctorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Doctor(models.Model):
    firstname = models.CharField(max_length=255, blank=False, null=False)
    lastname = models.CharField(max_length=255, blank=True, null=True)  
    specialty = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    contact = models.CharField(max_length=255, blank=True, null=True)  
    password = models.CharField(max_length=255, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)
    
    objects = DoctorManager()
    
    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
        
    def save(self, *args, **kwargs):
        if not self.pk or not check_password(self.password, self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
    def delete(self):
        self.is_deleted = True
        self.save()




