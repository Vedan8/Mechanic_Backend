from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from twilio.rest import Client
from Mechanic.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.utils.encoding import force_str
from .serializers import UserRegisterSerializer, UserLoginSerializer
from Detail.models import CustomerDetail,MechanicDetail


User = get_user_model()
OTP_STORAGE = {}


def send_sms(phone_number, otp):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    call = client.calls.create(
        twiml=f"<Response><Say>Your OTP code is {otp[0]} {otp[1]} {otp[2]} {otp[3]}. Please enter it to proceed.</Say></Response>",
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER
    )
    print(call.sid)

    return call.sid

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = str(random.randint(1000, 9999))
            print(otp)
            OTP_STORAGE[phone_number] = otp  
            # send_sms(phone_number, otp)
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        device_token = request.data.get('device_token')
        if(not phone_number or not otp or not password or not user_type):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if OTP_STORAGE.get(phone_number) == otp:
            user=User.objects.create_user(phone_number=phone_number, password=password, user_type=user_type, device_token=device_token)
            refresh = RefreshToken.for_user(user)
            del OTP_STORAGE[phone_number]
            return Response({'message': 'User registered successfully','access':str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            device_token = request.data.get("device_token")  # Get device_token from request data

            if device_token:
                user.device_token = device_token  # Update the device_token
                user.save(update_fields=["device_token"])  # Save the updated device_token

            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).first()
        customer = CustomerDetail.objects.filter(user=user).first()
        mechanic = MechanicDetail.objects.filter(user=user).first()
        email = None
        if customer:
            email = customer.email
        elif mechanic:
            email = mechanic.email

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"http://127.0.0.1:8000/api/reset-password/{uid}/{token}/"

            # Send OTP via SMS (Twilio or another SMS service)
            # send_sms(phone_number, f"Reset your password using this link: {reset_url}")

            # Send Email if available
            if email:
                send_mail("Password Reset", f"Click the link to reset your password: {reset_url}", "noreply@example.com", [email])

            return Response({'message': 'Reset link sent via SMS and Email (if available)'}, status=status.HTTP_200_OK)

        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


def reset_password_page(request, uidb64, token):
    if request.method == "GET":
        return render(request, "reset_password.html", {"uidb64": uidb64, "token": token})

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return HttpResponse("Passwords do not match", status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.password = make_password(new_password)
                user.save()
                return HttpResponse("Password reset successful", status=200)
            else:
                return HttpResponse("Invalid or expired token", status=400)

        except (User.DoesNotExist, ValueError, TypeError):
            return HttpResponse("Invalid request", status=400)