from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)
    
    class Meta:
        db_table = 'admins'  
    
    def __str__(self):
        return self.name