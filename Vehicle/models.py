from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary
from django.core.files.uploadedfile import InMemoryUploadedFile
from Users.models import User

# Create your models here.
class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=30, unique=True)
    vehicle_model = models.CharField(max_length=150)
    vehicle_type = models.CharField(max_length=150)
    fuel_type = models.CharField(max_length=150)
    vehicle_company = models.CharField(max_length=150)
    vehicle_image = CloudinaryField('image')
    vehicle_document = CloudinaryField('document',resource_type='raw')
    vehicle_image_url = models.URLField(max_length=500, blank=True, null=True)
    vehicle_document_url = models.URLField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        if isinstance(self.vehicle_image, InMemoryUploadedFile):
            upload_result = cloudinary.uploader.upload(self.vehicle_image)
            self.vehicle_image_url = upload_result.get('secure_url')
        if isinstance(self.vehicle_document, InMemoryUploadedFile):
            upload_result = cloudinary.uploader.upload(self.vehicle_document,resource_type='raw',type="upload",format="pdf")
            self.vehicle_document_url = upload_result.get('secure_url')

        super(Vehicle, self).save(*args, **kwargs)