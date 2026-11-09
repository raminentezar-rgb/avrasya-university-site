# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Thread, Message, Notification, SupportThread, SupportMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group_name = f'chat_{self.thread_id}'
        self.user = self.scope['user']
        self.has_access = False

        # بررسی احراز هویت، نقش (staff/professor) و عضویت در Thread
        if not self.user.is_authenticated or not await self.can_access_thread():
            await self.close()
            return

        self.has_access = True
        await self.channel_layer.group_add(
            self.thread_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if getattr(self, 'has_access', False):
            await self.channel_layer.group_discard(
                self.thread_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        if not getattr(self, 'has_access', False):
            await self.close()
            return

        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'message')

        if message_type == 'typing':
            await self.channel_layer.group_send(
                self.thread_group_name,
                {
                    'type': 'typing_status',
                    'user_id': self.user.id,
                    'username': self.user.get_full_name() or self.user.username,
                    'is_typing': text_data_json.get('is_typing', False)
                }
            )

        elif message_type == 'message':
            message = text_data_json.get('message', '').strip()
            file_url = text_data_json.get('file_url')

            if not message and not file_url:
                return

            msg = await self.save_message(message, file_url)
            if not msg:
                return

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

            await self.send_notification_to_others(message)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'file_url': event.get('file_url'),
            'file_name': event.get('file_name'),
            'file_size': event.get('file_size'),
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'created_at': event['created_at'],
            'created_at_full': event.get('created_at_full'),
            'message_id': event['message_id'],
            'is_read': event.get('is_read', False)
        }))

    async def typing_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
            'username': event['username'],
            'is_typing': event['is_typing']
        }))

    @database_sync_to_async
    def can_access_thread(self):
        if not hasattr(self.user, 'profile') or self.user.profile.role not in ('staff', 'professor'):
            return False
        try:
            thread_id_int = int(self.thread_id)
        except (ValueError, TypeError):
            return False
        return Thread.objects.filter(
            id=thread_id_int,
            participants=self.user,
            is_active=True
        ).exists()

    @database_sync_to_async
    def save_message(self, message, file_url):
        try:
            thread = Thread.objects.get(id=self.thread_id, participants=self.user, is_active=True)
        except Thread.DoesNotExist:
            return None
        msg = Message.objects.create(
            thread=thread,
            sender=self.user,
            text=message
        )
        return msg

    @database_sync_to_async
    def send_notification_to_others(self, message):
        """ارسال نوتیفیکیشن به سایر شرکت‌کنندگان"""
        try:
            thread = Thread.objects.get(id=self.thread_id, participants=self.user)
        except Thread.DoesNotExist:
            return
        other_users = thread.participants.exclude(id=self.user.id)

        for user in other_users:
            Notification.objects.create(
                user=user,
                notification_type='message',
                title=f'Yeni mesaj: {self.user.get_full_name() or self.user.username}',
                message=message[:50] + '...' if len(message) > 50 else message,
                thread_id=self.thread_id,
                sender_id=self.user.id
            )


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.notification_group_name = f'notifications_{self.user.id}'
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )
        await self.accept()

        unread_count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': unread_count
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'notification_group_name'):
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

            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': unread_count
            }))

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification_id': event['notification_id'],
            'title': event['title'],
            'message': event['message'],
            'thread_id': event.get('thread_id'),
            'sender_id': event.get('sender_id'),
            'created_at': event.get('created_at')
        }))

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


class SupportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_key = self.scope['url_route']['kwargs']['session_key']
        self.group_name = f'support_{self.session_key}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        if self.scope['user'].is_authenticated and self.scope['user'].is_staff:
            await self.channel_layer.group_add(
                'support_staff_notifications',
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
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
                msg = await self.save_support_message(text, sender_name)

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
        thread, _ = SupportThread.objects.get_or_create(
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

        thread.is_active = True
        thread.save()

        return msg
