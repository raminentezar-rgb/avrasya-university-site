from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name='threads')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        participants_names = [p.get_full_name() or p.username for p in self.participants.all()]
        return f"Thread: {' & '.join(participants_names)}"
    
    def get_other_participant(self, user):
        """Return the other participant in the thread"""
        for participant in self.participants.all():
            if participant.id != user.id:
                return participant
        return None
    
    def get_last_message(self):
        """Return the last message in the thread"""
        messages = list(self.messages.all())
        if not messages:
            return None
        return sorted(messages, key=lambda m: m.created_at, reverse=True)[0]

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/%Y/%m/%d/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message {self.id} by {self.sender.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update thread's updated_at using update() to avoid saving full object
        Thread.objects.filter(id=self.thread_id).update(updated_at=self.created_at)




# chat/models.py - اضافه کردن مدل نوتیفیکیشن

# chat/models.py - این کد را به انتهای فایل اضافه کنید

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('message', 'پیام جدید'),
        ('mention', 'منشن'),
        ('system', 'سیستم'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='message')
    title = models.CharField(max_length=255)
    message = models.TextField()
    thread_id = models.IntegerField(null=True, blank=True)
    sender_id = models.IntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.user.username}: {self.title[:50]}"

class SupportThread(models.Model):
    session_key = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    language = models.CharField(max_length=10, default='tr')
    assigned_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_support_threads')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Support Thread'
        verbose_name_plural = 'Support Threads'
        ordering = ['-updated_at']

    def __str__(self):
        return f'SupportSession: {self.full_name or self.session_key} ({self.language})'


class SupportMessage(models.Model):
    thread = models.ForeignKey(SupportThread, on_delete=models.CASCADE, related_name='support_messages')
    sender_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sender_name = models.CharField(max_length=255)
    text = models.TextField()
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Support Message'
        verbose_name_plural = 'Support Messages'
        ordering = ['created_at']
