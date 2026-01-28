from django.db import models
from django.contrib.auth.models import User


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
        ('open', 'Open'),
        ('answered', 'Answered'),
        ('closed', 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.ticket.subject}"
    


# models.py
class KnowledgeBase(models.Model):
    CONTENT_TYPES = [
        ('faq', 'FAQ'),
        ('guide', 'راهنما'),
        ('policy', 'قوانین و مقررات'),
        ('service', 'خدمات دانشگاه'),
        ('announcement', 'اطلاعیه'),
        ('contact', 'اطلاعات تماس'),
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




