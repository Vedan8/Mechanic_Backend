from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number','user_type','device_token']
        extra_kwargs = {'device_token': {'required': False}}

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    device_token = serializers.CharField(write_only=True, required=False)

    def validate(self, data):
        user = authenticate(phone_number=data['phone_number'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


