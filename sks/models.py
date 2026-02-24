from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    """Haber ve duyuru kategorileri"""
    name = models.CharField(_('Kategori Adı'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True)
    is_active = models.BooleanField(_('Aktif'), default=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Kategori')
        verbose_name_plural = _('Kategoriler')
        ordering = ['name']

    def __str__(self):
        return self.name


class News(models.Model):
    """Haber modeli"""
    NEWS_TYPE_CHOICES = [
        ('news', _('Haber')),
        ('announcement', _('Duyuru')),
        ('event', _('Etkinlik')),
        ('achievement', _('Başarı')),
    ]

    title = models.CharField(_('Başlık'), max_length=250)
    slug = models.SlugField(_('Slug'), unique=True, max_length=250)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_('Kategori'),
        related_name='news'
    )
    news_type = models.CharField(
        _('Haber Türü'), 
        max_length=20, 
        choices=NEWS_TYPE_CHOICES,
        default='news'
    )
    
    # Ana görsel
    image = models.ImageField(
        _('Görsel'), 
        upload_to='sks/news/%Y/%m/',
        blank=True,
        null=True,
        help_text=_('Haber ana görseli (Önerilen boyut: 800x400 piksel)')
    )
    image_alt = models.CharField(
        _('Görsel Alternatif Metni'), 
        max_length=255, 
        blank=True,
        help_text=_('SEO ve erişilebilirlik için')
    )
    
    # İçerik
    summary = models.TextField(
        _('Özet'), 
        max_length=500,
        help_text=_('Kartlarda gösterilecek kısa özet (Maksimum 500 karakter)')
    )
    content = models.TextField(_('İçerik'))
    
    # Meta veriler
    is_featured = models.BooleanField(_('Öne Çıkan'), default=False)
    is_published = models.BooleanField(_('Yayında'), default=True)
    published_at = models.DateTimeField(
        _('Yayın Tarihi'), 
        default=timezone.now,
        help_text=_('Haberin yayınlanma zamanı')
    )
    
    # İstatistikler
    views_count = models.PositiveIntegerField(_('Görüntülenme Sayısı'), default=0)
    
    # Zaman damgaları
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    # Yazar
    author = models.CharField(
        _('Yazar'), 
        max_length=100, 
        blank=True,
        help_text=_('Yazar adı veya haber kaynağı')
    )

    class Meta:
        verbose_name = _('Haber')
        verbose_name_plural = _('Haberler')
        ordering = ['-is_featured', '-published_at']
        indexes = [
            models.Index(fields=['-published_at', 'is_published']),
            models.Index(fields=['news_type', 'is_published']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sks:news_detail', args=[self.slug])

    def get_image_url(self):
        """Görsel URL'sini veya varsayılan görseli döndür"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/core/img/default-news.jpg'
    
    def get_news_type_display_with_icon(self):
        """Haber türünü ve ikonunu döndür"""
        icons = {
            'news': 'fas fa-newspaper',
            'announcement': 'fas fa-bullhorn',
            'event': 'fas fa-calendar-alt',
            'achievement': 'fas fa-trophy',
        }
        return {
            'type': self.get_news_type_display(),
            'icon': icons.get(self.news_type, 'fas fa-info-circle')
        }


class Announcement(models.Model):
    """Duyuru modeli"""
    title = models.CharField(_('Başlık'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=250, unique=True, blank=True)
    content = models.TextField(_('İçerik'))
    summary = models.TextField(
        _('Özet'), 
        max_length=300, 
        blank=True,
        help_text=_('Listelerde gösterilecek kısa özet')
    )
    
    # İsteğe bağlı görsel
    image = models.ImageField(
        _('Görsel'), 
        upload_to='sks/announcements/%Y/%m/',
        blank=True,
        null=True
    )
    
    # İsteğe bağlı dış link
    external_link = models.URLField(_('Dış Link'), blank=True, null=True)
    external_link_text = models.CharField(_('Dış Link Metni'), max_length=50, blank=True)
    
    # Tarih
    announcement_date = models.DateField(_('Duyuru Tarihi'), default=timezone.now)
    is_important = models.BooleanField(_('Önemli'), default=False)
    is_active = models.BooleanField(_('Aktif'), default=True)
    
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('Duyuru')
        verbose_name_plural = _('Duyurular')
        ordering = ['-is_important', '-announcement_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sks:announcement_detail', args=[self.slug])

    def get_day(self):
        """Günü döndür (kutuda göstermek için)"""
        return self.announcement_date.day

    def get_month_short(self):
        """Ayı kısaltılmış olarak döndür"""
        months = {
            1: 'Oca', 2: 'Şub', 3: 'Mar', 4: 'Nis',
            5: 'May', 6: 'Haz', 7: 'Tem', 8: 'Ağu',
            9: 'Eyl', 10: 'Eki', 11: 'Kas', 12: 'Ara'
        }
        return months.get(self.announcement_date.month, '')

    def get_image_url(self):
        """Görsel URL'sini döndür"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None