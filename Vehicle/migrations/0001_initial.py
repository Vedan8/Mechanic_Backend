# Generated by Django 5.1.7 on 2025-03-23 13:39

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_number', models.CharField(max_length=30, unique=True)),
                ('vehicle_model', models.CharField(max_length=150)),
                ('vehicle_type', models.CharField(max_length=150)),
                ('fuel_type', models.CharField(max_length=150)),
                ('vehicle_company', models.CharField(max_length=150)),
                ('vehicle_image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('vehicle_document', cloudinary.models.CloudinaryField(max_length=255, verbose_name='document')),
                ('vehicle_image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('vehicle_document_url', models.URLField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
