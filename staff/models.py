from django.db import models

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
    firstname = models.CharField(max_length=255, blank=False, null=False,default='first_name')
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
    role = models.ForeignKey(Roles, on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'staff_action'
        
    def __str__(self):
        return self.name
    