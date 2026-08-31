from django.db import models
from django.urls import reverse

class SliderItem(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('image', 'Resim'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Başlık")
    content_type = models.CharField(
        max_length=10, 
        choices=CONTENT_TYPE_CHOICES, 
        default='image',
        verbose_name="İçerik Türü"
    )
    image = models.ImageField(
        upload_to='slider/', 
        blank=True, 
        null=True,
        verbose_name="Resim"
    )
    video = models.FileField(
        upload_to='slider/videos/',
        blank=True,
        null=True,
        verbose_name="Video Dosyası"
    )
    video_url = models.URLField(
        blank=True,
        verbose_name="Video Linki (YouTube, Vimeo, vs.)"
    )
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f"Slider #{self.id}" if self.id else "Yeni Slider"

    def get_media_url(self):
        """برگرداندن URL رسانه بر اساس نوع محتوا"""
        if self.content_type == 'video' and self.video:
            return self.video.url
        elif self.content_type == 'image' and self.image:
            return self.image.url
        return None

class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:page_detail', args=[self.slug])
    












class QuestionAnswer(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.question
