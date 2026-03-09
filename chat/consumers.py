# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Thread, Message, Notification

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group_name = f'chat_{self.thread_id}'
        self.user = self.scope['user']
        
        # Check if user is authenticated
        if not self.user.is_authenticated:
            await self.close()
        else:
            # Join thread group
            await self.channel_layer.group_add(
                self.thread_group_name,
                self.channel_name
            )
            await self.accept()
    
    async def disconnect(self, close_code):
        # Leave thread group
        await self.channel_layer.group_discard(
            self.thread_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'message')
        
        if message_type == 'typing':
            # Broadcast typing status
            await self.channel_layer.group_send(
                self.thread_group_name,
                {
                    'type': 'typing_status',
                    'user_id': self.user.id,
                    'username': self.user.get_full_name() or self.user.username,
                    'is_typing': text_data_json['is_typing']
                }
            )
        
        elif message_type == 'message':
            message = text_data_json['message']
            file_url = text_data_json.get('file_url')
            
            # Save message to database
            msg = await self.save_message(message, file_url)
            
            # Broadcast message to group
            await self.channel_layer.group_send(
                self.thread_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'file_url': file_url,
                    'sender_id': self.user.id,
                    'sender_name': self.user.get_full_name() or self.user.username,
                    'created_at': msg.created_at.strftime('%H:%M'),
                    'message_id': msg.id
                }
            )
            
            # Send notification to other participants
            await self.send_notification_to_others(message)
    
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'file_url': event.get('file_url'),
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'created_at': event['created_at'],
            'message_id': event['message_id']
        }))
    
    async def typing_status(self, event):
        # Send typing status to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
            'username': event['username'],
            'is_typing': event['is_typing']
        }))
    
    @database_sync_to_async
    def save_message(self, message, file_url):
        thread = Thread.objects.get(id=self.thread_id)
        msg = Message.objects.create(
            thread=thread,
            sender=self.user,
            text=message
        )
        return msg
    
    @database_sync_to_async
    def send_notification_to_others(self, message):
        """ارسال نوتیفیکیشن به سایر شرکت‌کنندگان"""
        thread = Thread.objects.get(id=self.thread_id)
        other_users = thread.participants.exclude(id=self.user.id)
        
        for user in other_users:
            # Create notification in database
            Notification.objects.create(
                user=user,
                notification_type='message',
                title=f'پیام جدید از {self.user.get_full_name() or self.user.username}',
                message=message[:50] + '...' if len(message) > 50 else message,
                thread_id=self.thread_id,
                sender_id=self.user.id
            )


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.notification_group_name = f'notifications_{self.user.id}'
        
        if not self.user.is_authenticated:
            await self.close()
        else:
            # Join notification group
            await self.channel_layer.group_add(
                self.notification_group_name,
                self.channel_name
            )
            await self.accept()
            
            # Send unread notifications count
            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': unread_count
            }))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        
        if action == 'mark_read':
            notification_id = text_data_json.get('notification_id')
            await self.mark_notification_read(notification_id)
            
            # Send updated count
            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': unread_count
            }))
    
    async def send_notification(self, event):
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification_id': event['notification_id'],
            'title': event['title'],
            'message': event['message'],
            'thread_id': event.get('thread_id'),
            'sender_id': event.get('sender_id'),
            'created_at': event.get('created_at')
        }))
        
        # Also try to send browser notification
        await self.send(text_data=json.dumps({
            'type': 'browser_notification',
            'title': event['title'],
            'message': event['message'],
            'thread_id': event.get('thread_id')
        }))
    
    @database_sync_to_async
    def get_unread_count(self):
        return Notification.objects.filter(user=self.user, is_read=False).count()
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        Notification.objects.filter(id=notification_id, user=self.user).update(is_read=True)