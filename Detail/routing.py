from django.urls import path
from .consumers import MechanicNotificationConsumer,LocationConsumer

websocket_urlpatterns = [
    path("ws/notifications/", MechanicNotificationConsumer.as_asgi()),
    path("ws/location/<int:request_id>/", LocationConsumer.as_asgi()),
]
