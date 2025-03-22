from django.urls import path
from .views import CustomerDetailView, UserDetailView,MechanicDetailView, CustomerDetailPatchView,ServiceRequestView
urlpatterns = [
    path('customers/', CustomerDetailView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailPatchView.as_view(), name='customer-detail'),
    path('userprofile/', UserDetailView.as_view(), name='customer-detail'),
    path('mechanics/', MechanicDetailView.as_view(), name='mechanic-list-create'),
    path('service-requests/', ServiceRequestView.as_view(), name='service-request-list-create'),
]
