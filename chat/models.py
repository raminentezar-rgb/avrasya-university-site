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
        return self.participants.exclude(id=user.id).first()
    
    def get_last_message(self):
        """Return the last message in the thread"""
        return self.messages.order_by('-created_at').first()

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
        # Update thread's updated_at when new message is created
        self.thread.updated_at = self.created_at
        self.thread.save()