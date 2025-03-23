# Generated by Django 5.1.7 on 2025-03-23 13:39

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('gender', models.CharField(blank=True, max_length=150, null=True)),
                ('aadhar_card', models.CharField(blank=True, max_length=15, null=True)),
                ('aadhar_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('aadhar_image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('driving_license', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=150)),
                ('address', models.TextField(blank=True, null=True)),
                ('preferred_mechanic', models.CharField(blank=True, max_length=150, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('secondary_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('latitude', models.CharField(blank=True, max_length=150, null=True)),
                ('longitude', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MechanicDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('gender', models.CharField(max_length=150)),
                ('aadhar_card', models.CharField(max_length=15)),
                ('aadhar_image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('aadhar_image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('service_type', models.CharField(max_length=150)),
                ('experience', models.IntegerField()),
                ('average_rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('available', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=150)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(blank=True, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('problem', models.TextField()),
                ('latitude', models.CharField(max_length=150)),
                ('longitude', models.CharField(max_length=150)),
                ('woman_children', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Completed', 'Completed'), ('Ongoing', 'Ongoing')], default='Active', max_length=150)),
            ],
        ),
    ]
