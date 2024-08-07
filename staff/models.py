from django.db import models
from doctor.models import Doctor
from patient.models import Patient, Room
from . helper import generate_random_string

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
    firstname = models.CharField(max_length=255, blank=False, null=False, default='')
    lastname = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, default=1)
    city = models.CharField(max_length=50, blank=False, null=False, default='')
    joined = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=255, blank=False, null=True, unique=True)
    password = models.CharField(max_length=255, blank=False, null=False, default='')
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
    description = models.CharField(max_length=255)
    url_name = models.CharField(max_length=100, default="")

    class Meta:
        db_table = 'staff_action'

    def __str__(self):
        return f"{self.name} {self.role} {self.description} {self.url_name}"
    
    
class StaffActionRoles(models.Model):
    action = models.ForeignKey(StaffAction, on_delete=models.CASCADE, default=1)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, default=1)
    
    class Meta:
        db_table = 'staff_action_roles'



class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    instructions = models.TextField(blank=True)
    created_by = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prescriptions'
        

        
        
class SugarTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True,blank=True,default=None)
    investigation = models.CharField(max_length=255, default='Fasting Blood Sugar, Postprandial Blood Sugar, Random Blood Sugar, HbA1c, Oral Glucose Tolerance Test (OGTT)')
    result = models.CharField(max_length=255)
    reference_value = models.CharField(max_length=255, default='70 - 100, 70 - 140, 70 - 140, 4.0 - 5.6, 140 - 199')
    unit = models.CharField(max_length=255, default='mg/dL, mg/dL, mg/dL, %, mg/dL')
    price = models.IntegerField(default=150)
    is_completed = models.BooleanField(default=False)
    

    class Meta:
        db_table = 'sugar_test'
    def __str__(self):
        return f"Investigation: {self.investigation}"
    
class ST(models.Model):
    investigation = models.CharField(max_length=50)
    reference_value = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
   
    class Meta:
        db_table = 'st'
        

class LiverFunctionTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True,blank=True,default=None)
    price = models.IntegerField(default=670)
    is_completed = models.BooleanField(default=False)
    investigation = models.CharField(max_length=255,default='Total Bilirubin, Direct Bilirubin, Indirect Bilirubin, Aspartate Aminotransferase (AST/SGOT), Alanine Aminotransferase (ALT/SGPT), Alkaline Phosphatase (ALP), Total Protein, Albumin, Globulin, Albumin/Globulin Ratio')
    result =models.CharField(max_length=255)
    reference_value = models.CharField(max_length=255,default='0.1 - 1.2, 0.0 - 0.4, 0.1 - 0.8, 5 - 40, 7 - 56, 30 - 120, 6.0 - 8.3, 3.5 - 5.0, 2.0 - 3.5, 1.0 - 2')
    unit = models.CharField(max_length=255,default='mg/dL, mg/dL, mg/dL, U/L, U/L, U/L, g/dL, g/dL, g/dL, ratio')


    class Meta:
        db_table = 'liver_function_test'
        
    def __str__(self):
        return self.investigation

class LFT(models.Model):

    investigation = models.CharField(max_length=50)
    reference_value = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'lft'
        
class CholesterolTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True,blank=True,default=None)
    price = models.IntegerField(default=450)
    is_completed = models.BooleanField(default=False)
    investigation = models.CharField(
        max_length=255,
        default='Total Cholesterol, LDL Cholesterol (Low-Density Lipoprotein), HDL Cholesterol (High-Density Lipoprotein), Triglycerides'
    )
    result =models.CharField(max_length=255,default='')
    reference_value = models.CharField(
        max_length=255,
        default='< 200, < 100, > 40, < 150'
    )
    unit = models.CharField(
        max_length=255,
        default='mg/dL, mg/dL, mg/dL, mg/dL'
    )
    price = models.IntegerField(default=450)
    

    class Meta:
        db_table = 'cholesterol_test'
        
    def __str__(self):
        return self.investigation
    
class CT(models.Model):

    investigation = models.CharField(max_length=50)
    reference_value = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'ct'
        
class KidneyFunctionTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True,default=None)
    price = models.IntegerField(default=935)
    is_completed = models.BooleanField(default=False)
    investigation = models.CharField(
        max_length=255,
        default='Urea, Creatinine, Uric Acid, Calcium, Total, Phosphorus, Alkaline Phosphatase (ALP), Total Protein, Albumin, Sodium, Potassium, Chloride'
    )
    reference_value = models.CharField(
        max_length=255,
        default='13 - 43, 0.7 - 1.3, 3.5 - 7.2, 8.7 - 10.4, 2.4 - 5.1, 30 - 120, 5.7 - 8.2, 3.2 - 4.8, 136 - 145, 3.5 - 5.1, 98 - 107'
    )
    result =models.CharField(max_length=255, default='')
    unit = models.CharField(
        max_length=255,
        default='mg/dL, mg/dL, mg/dL, mg/dL, mg/dL, U/L, g/dL, g/dL, mEq/L, mEq/L, mEq/L'
    )
    
    class Meta:
        db_table = 'kidney_function_test'
        
    def __str__(self):
        return self.investigation
    
class KFT(models.Model):
    investigation = models.CharField(max_length=50)
    reference_value = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'kft'
        
    
    
    
    
class LabReport(models.Model):
    CATEGORY_CHOICES = [
        ('Sugar Test', 'Sugar Test'),
        ('Cholesterol Test', 'Cholesterol Test'),
        ('Liver Test', 'Liver Test'),
        ('Kidney Test', 'Kidney Test'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liver_test = models.ForeignKey(LiverFunctionTest, on_delete=models.CASCADE, null=True, blank=True)
    kidney_test = models.ForeignKey(KidneyFunctionTest, on_delete=models.CASCADE, null=True, blank=True)
    sugar_test = models.ForeignKey(SugarTest, on_delete=models.CASCADE, null=True, blank=True)
    cholesterol_test = models.ForeignKey(CholesterolTest, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'lab_report'
        
        
        
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    strength = models.CharField(max_length=50)
    expiry_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = 'medicine'

class PatientBills(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE, null=True, blank=True)
    medicine_bill = models.IntegerField(default=0)
    lab_report_bill = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    class Meta:
        db_table = 'patient_bills'
#__________________________________________INVOICE_____________________________________________

class Invoice(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('paypal', 'PayPal'),
        ('razorpay', 'Razorpay')
    ]
    invoice_no = models.CharField(max_length=50)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room_charges = models.IntegerField(null=True, blank=True)
    bill_id = models.ForeignKey(PatientBills,on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50,default='pending')
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'invoice'

    def __str__(self):
        return self.invoice_no
    

class UserOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} - {self.otp}'