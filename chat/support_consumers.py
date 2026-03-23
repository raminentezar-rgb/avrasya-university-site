import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import SupportThread, SupportMessage, Notification

class SupportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_key = self.scope['url_route']['kwargs']['session_key']
        self.group_name = f'support_{self.session_key}'

        # Join support group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        # If user is staff, join staff notifications group
        if self.scope['user'].is_authenticated and self.scope['user'].is_staff:
            await self.channel_layer.group_add(
                'support_staff_notifications',
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave support group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
        if self.scope['user'].is_authenticated and self.scope['user'].is_staff:
            await self.channel_layer.group_discard(
                'support_staff_notifications',
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'message')

        if message_type == 'message':
            text = data.get('message', '').strip()
            sender_name = data.get('sender_name', 'Ziyaretçi')
            
            if text:
                # Save message
                msg = await self.save_support_message(text, sender_name)
                
                # Broadcast message to the group
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'chat_message',
                        'message': text,
                        'sender_name': sender_name,
                        'is_staff': self.scope['user'].is_authenticated and self.scope['user'].is_staff,
                        'created_at': msg.created_at.strftime('%H:%M')
                    }
                )
                
                # If visitor sends message, notify staff group
                if not (self.scope['user'].is_authenticated and self.scope['user'].is_staff):
                    await self.channel_layer.group_send(
                        'support_staff_notifications',
                        {
                            'type': 'staff_notification',
                            'session_key': self.session_key,
                            'visitor_name': sender_name,
                            'message': text[:50]
                        }
                    )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender_name': event['sender_name'],
            'is_staff': event['is_staff'],
            'created_at': event['created_at']
        }))

    async def staff_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_support_request',
            'session_key': event['session_key'],
            'visitor_name': event['visitor_name'],
            'message': event['message']
        }))

    @database_sync_to_async
    def save_support_message(self, text, sender_name):
        thread, created = SupportThread.objects.get_or_create(
            session_key=self.session_key,
            defaults={'full_name': sender_name}
        )
        
        is_staff = self.scope['user'].is_authenticated and self.scope['user'].is_staff
        
        msg = SupportMessage.objects.create(
            thread=thread,
            sender_user=self.scope['user'] if is_staff else None,
            sender_name=sender_name,
            text=text,
            is_staff=is_staff
        )
        
        # Update thread
        thread.is_active = True
        thread.save()
        
        return msg
