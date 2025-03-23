from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from django.apps import apps
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Dictionary to track online mechanics
online_mechanics = {}

class MechanicNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        self.mechanic = None
        if token:
            try:
                access_token = AccessToken(token)

                # Ensure channel layer is ready before continuing
                await self.ensure_channel_layer_ready()

                # Dynamically import User model when needed
                User = apps.get_model('Users', 'User')

                # Retry fetching the user with exponential backoff
                self.mechanic = await self.retry_get_user(User, access_token["user_id"])

            except Exception:
                await self.close()
                return

        if not self.mechanic:
            await self.close(code=403)
            return

        self.group_name = f"mechanic_{self.mechanic.id}"
        online_mechanics[self.mechanic.id] = True  # Mark mechanic as online

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"connected": True}))

    async def disconnect(self, close_code):
        if self.mechanic and self.mechanic.id in online_mechanics:
            del online_mechanics[self.mechanic.id]  # Remove mechanic from online list
        
        if self.mechanic:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def get_user(self, User, user_id):
        """ Fetch user from the database, handling exceptions properly. """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    async def retry_get_user(self, User, user_id, max_retries=5, delay=0.5):
        """
        Retry getting user with exponential backoff to avoid database race conditions.
        """
        for i in range(max_retries):
            user = await self.get_user(User, user_id)
            if user:
                return user
            await asyncio.sleep(delay * (2 ** i))  # Exponential backoff
        return None

    async def ensure_channel_layer_ready(self, max_retries=5, delay=0.5):
        """
        Ensures that the channel layer is properly initialized before proceeding.
        """
        for _ in range(max_retries):
            if self.channel_layer is not None:
                return
            await asyncio.sleep(delay)


class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.service_request_id = self.scope['url_route']['kwargs']['request_id']
        self.room_group_name = f'location_{self.service_request_id}'

        # Extract and validate token
        token = self.get_token_from_scope()
        if not token:
            await self.close()
            return

        # Ensure the channel layer is ready before continuing
        await self.ensure_channel_layer_ready()

        # Dynamically import User model when needed
        User = apps.get_model('Users', 'User')

        # Decode token and get user with retry mechanism
        self.user = await self.retry_get_user_from_token(User, token)

        if not self.user:
            await self.close()
            return

        self.user_type = self.user.user_type  # Assuming usertype field exists in your model

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Broadcast location update with assigned user_type
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_location',
                'user_type': self.user_type,
                'latitude': latitude,
                'longitude': longitude
            }
        )

    async def send_location(self, event):
        await self.send(text_data=json.dumps({
            'user_type': event['user_type'],
            'latitude': event['latitude'],
            'longitude': event['longitude']
        }))

    def get_token_from_scope(self):
        """ Extract JWT token from query parameters or headers. """
        query_string = self.scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]  # Extract from query params

        if not token:
            headers = dict(self.scope["headers"])
            auth_header = headers.get(b'authorization', b'').decode()
            if auth_header.startswith("Bearer "):
                token = auth_header.split("Bearer ")[1]  # Extract from headers
        
        return token

    @database_sync_to_async
    def get_user_from_token(self, User, token):
        """ Decode JWT token and return user instance. """
        try:
            decoded_data = UntypedToken(token)  # Decode JWT
            user_id = decoded_data["user_id"]
            return User.objects.get(id=user_id)
        except (InvalidToken, TokenError, User.DoesNotExist):
            return None

    async def retry_get_user_from_token(self, User, token, max_retries=5, delay=0.5):
        """
        Retry fetching user from token with exponential backoff.
        """
        for i in range(max_retries):
            user = await self.get_user_from_token(User, token)
            if user:
                return user
            await asyncio.sleep(delay * (2 ** i))  # Exponential backoff
        return None

    async def ensure_channel_layer_ready(self, max_retries=5, delay=0.5):
        """
        Ensures that the channel layer is properly initialized before proceeding.
        """
        for _ in range(max_retries):
            if self.channel_layer is not None:
                return
            await asyncio.sleep(delay)
