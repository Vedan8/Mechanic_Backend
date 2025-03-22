from rest_framework import generics
from .models import CustomerDetail,MechanicDetail,ServiceRequest
from .serializers import CustomerDetailSerializer,MechanicDetailSerializer,ServiceRequestSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

class ServiceRequestView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = CustomerDetail.objects.filter(user=self.request.user).first()
        return ServiceRequest.objects.filter(customer=customer)

    def perform_create(self, serializer):
        customer = CustomerDetail.objects.filter(user=self.request.user).first()
        serializer.save(customer=customer)