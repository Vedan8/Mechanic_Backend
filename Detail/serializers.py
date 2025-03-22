from rest_framework import serializers
from .models import CustomerDetail, MechanicDetail,ServiceRequest


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetail
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

class MechanicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MechanicDetail
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'