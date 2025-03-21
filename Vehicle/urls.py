from django.urls import path
from .views import VehicleListCreateView, VehicleRetrieveUpdateDeleteView

urlpatterns = [
    path('vehicles/', VehicleListCreateView.as_view(), name='vehicle-list-create'),
    path('vehicles/<int:pk>/', VehicleRetrieveUpdateDeleteView.as_view(), name='vehicle-detail'),
]
