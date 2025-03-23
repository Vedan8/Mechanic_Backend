from rest_framework import generics
from .models import CustomerDetail,MechanicDetail,ServiceRequest
from .serializers import CustomerDetailSerializer,MechanicDetailSerializer,ServiceRequestSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from fcm_django.models import FCMDevice
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification
from Users.models import User
from .consumers import online_mechanics
from firebase_admin import messaging
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

class CustomerDetailView(generics.ListCreateAPIView):
    queryset = CustomerDetail.objects.all()
    serializer_class = CustomerDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerDetail.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,phone_number=self.request.user.phone_number)

class CustomerDetailPatchView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerDetail.objects.all()
    serializer_class = CustomerDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerDetail.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()

        # Check if all fields (except `verified` and `id`) are non-null
        fields_to_check = [
            "name", "gender", "aadhar_card", "aadhar_image", "aadhar_image_url",
            "driving_license", "email", "address", "preferred_mechanic",
            "phone_number", "secondary_phone_number"
        ]
        
        if all(getattr(instance, field) is not None for field in fields_to_check):
            instance.verified = True
            instance.save(update_fields=["verified"])

class MechanicDetailView(generics.ListCreateAPIView):
    queryset = MechanicDetail.objects.all()
    serializer_class = MechanicDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MechanicDetail.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,phone_number=self.request.user.phone_number)

class UserDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.user_type == 'Customer':
            customer = CustomerDetail.objects.filter(user=user).first()
            if customer:
                return Response(CustomerDetailSerializer(customer).data)
        elif user.user_type == 'Mechanic':
            mechanic = MechanicDetail.objects.filter(user=user).first()
            if mechanic:
                return Response(MechanicDetailSerializer(mechanic).data)
        
        return Response({'detail': 'User details not found'}, status=404)

class ServiceRequestView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceRequestSerializer

    def perform_create(self, serializer):
        customer = CustomerDetail.objects.filter(user=self.request.user).first()
        service_request = serializer.save(customer=customer)

        mechanics = User.objects.filter(user_type='Mechanic')
        channel_layer = get_channel_layer()

        for mechanic in mechanics:
            Notification.objects.create(mechanic=mechanic, message=service_request.problem)

            if self.is_mechanic_online(mechanic):  # Now checks dictionary
                async_to_sync(channel_layer.group_send)(
                    f"mechanic_{mechanic.id}",
                    {"type": "send_notification", "message": service_request.problem},
                )
            else:
                self.send_push_notification(token=self.request.user.device_token,title="New Service Request",body=service_request.problem)

    def is_mechanic_online(self, mechanic):
        return mechanic.id in online_mechanics  # Check dictionary

    def send_push_notification(self, token, title, body):
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token  # The FCM token of the user's device
        )

        try:
            response = messaging.send(message)
            print("Notification sent successfully:", response)
            return response
        except Exception as e:
            print("Error sending notification:", e)

@api_view(["POST"])
def accept_service_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    
    # Assign mechanic and change status
    mechanic = get_object_or_404(MechanicDetail, user=request.user)
    service_request.mechanic = mechanic
    service_request.status = "Ongoing"
    service_request.save()

    return Response({"message": "Service request accepted.", "service_request":ServiceRequestSerializer(service_request).data})