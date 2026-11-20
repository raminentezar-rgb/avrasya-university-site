import os
import secrets
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)

    staff = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='department',
        limit_choices_to={'is_staff': True},
        null=True,
        blank=True
    )

    email = models.EmailField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question



class Ticket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Açık'),
        ('answered', 'Yanıtlandı'),
        ('closed', 'Kapalı'),
    )
    PRIORITY_CHOICES = (
        ('low', 'Düşük'),
        ('medium', 'Orta'),
        ('high', 'Yüksek'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_name = models.CharField(max_length=150, blank=True)
    guest_email = models.EmailField(blank=True)
    guest_phone = models.CharField(max_length=30, blank=True)
    tracking_code = models.CharField(max_length=24, unique=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    attachment = models.FileField(upload_to='support/attachments/%Y/%m/%d/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def requester_name(self):
        if self.guest_name:
            return self.guest_name
        if self.user:
            return self.user.get_full_name() or self.user.username
        return "Ziyaretçi"

    @property
    def requester_email(self):
        if self.guest_email:
            return self.guest_email
        if self.user and self.user.email:
            return self.user.email
        return ""

    @property
    def attachment_name(self):
        return os.path.basename(self.attachment.name) if self.attachment else ""

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            year = timezone.now().year
            while True:
                candidate = f"AVU-{year}-{secrets.token_hex(4).upper()}"
                if not Ticket.objects.filter(tracking_code=candidate).exists():
                    self.tracking_code = candidate
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        prefix = f"[{self.tracking_code}] " if self.tracking_code else ""
        return f"{prefix}{self.subject}"


class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sender_name = models.CharField(max_length=150, blank=True)
    is_staff_reply = models.BooleanField(default=True)
    message = models.TextField()
    attachment = models.FileField(upload_to='support/reply_attachments/%Y/%m/%d/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def display_sender(self):
        if self.sender_name:
            return self.sender_name
        if self.staff:
            return self.staff.get_full_name() or self.staff.username
        return self.ticket.requester_name if not self.is_staff_reply else "Destek Birimi"

    @property
    def attachment_name(self):
        return os.path.basename(self.attachment.name) if self.attachment else ""

    def __str__(self):
        return f"Reply to {self.ticket.subject}"
    


# models.py
class KnowledgeBase(models.Model):
    CONTENT_TYPES = [
        ('faq', 'SSS'),
        ('guide', 'Rehber'),
        ('policy', 'Yönetmelik ve Kurallar'),
        ('service', 'Üniversite Hizmetleri'),
        ('announcement', 'Duyuru'),
        ('contact', 'İletişim Bilgileri'),
    ]
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag')
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

class ImportantLink(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    order = models.IntegerField(default=0)




