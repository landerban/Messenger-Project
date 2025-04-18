import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, CustomUser
from django.conf import settings
from cryptography.fernet import Fernet

fernet = Fernet(settings.FERNET_KEY)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']
        recipient_id = data['recipient_id']

        sender = await self.get_user(sender_id)
        recipient = await self.get_user(recipient_id)

        if sender and recipient:
            await self.save_message(sender, recipient, message)
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            })

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        await self.send(text_data=json.dumps({'message': message, 'sender_id': sender_id}))

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, sender, recipient, content):
        msg = Message(sender=sender, recipient=recipient)
        msg.set_content(content)
        msg.save()