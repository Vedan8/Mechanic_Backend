from email.policy import default
from django.db import models
from Vehicle.models import Vehicle
from Users.models import User
from cloudinary.models import CloudinaryField
import cloudinary
from django.core.files.uploadedfile import InMemoryUploadedFile

class CustomerDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=150, null=True, blank=True)
    aadhar_card = models.CharField(max_length=15, null=True, blank=True) 
    aadhar_image = CloudinaryField('image',null=True, blank=True)
    aadhar_image_url = models.URLField(max_length=500, blank=True, null=True)
    driving_license = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=150)
    address = models.TextField(null=True, blank=True)
    preferred_mechanic = models.CharField(max_length=150,null=True, blank=True)
    verified=models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15,null=True, blank=True)
    secondary_phone_number = models.CharField(max_length=15,null=True, blank=True)

    def save(self, *args, **kwargs):
        if isinstance(self.aadhar_image, InMemoryUploadedFile):
            upload_result = cloudinary.uploader.upload(self.aadhar_image)
            self.aadhar_image_url = upload_result.get('secure_url')
        super(CustomerDetail, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class MechanicDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=150)
    aadhar_card = models.CharField(max_length=15)
    aadhar_image = CloudinaryField('image')
    aadhar_image_url = models.URLField(max_length=500, blank=True, null=True)
    service_type=models.CharField(max_length=150)
    experience=models.IntegerField()
    average_rating=models.DecimalField(max_digits=2, decimal_places=1,null=True, blank=True)
    available = models.BooleanField(default=True)
    email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=15,null=True, blank=True)
    address = models.CharField(max_length=150)
    latitude= models.DecimalField(max_digits=10, decimal_places=10,null=True, blank=True)
    longitude= models.DecimalField(max_digits=10, decimal_places=10, null=True,blank=True)

    def save(self, *args, **kwargs):
        if isinstance(self.aadhar_image, InMemoryUploadedFile):
            upload_result = cloudinary.uploader.upload(self.aadhar_image)
            self.aadhar_image_url = upload_result.get('secure_url')
        super(MechanicDetail, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    customer = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE,null=True, blank=True)
    mechanic = models.ForeignKey(MechanicDetail, on_delete=models.CASCADE,null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    feedback = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    problem = models.TextField()
    latitude = models.CharField(max_length=150)
    longitude = models.CharField(max_length=150)
    status = models.CharField(max_length=150,choices=[('Active', 'Active'), ('Completed', 'Completed'),('Ongoing', 'Ongoing')], default='Active')

    def __str__(self):
        return f"Service Request for {self.vehicle.vehicle_number} by {self.customer.name}"

