from django.db import models
from django.urls import reverse

class GalleryCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Kategori Adı')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    cover_image = models.ImageField(upload_to='gallery/categories/', blank=True, null=True, verbose_name='Kapak Görseli')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    order = models.PositiveIntegerField(default=0, verbose_name='Gösterim Sırası')
    
    class Meta:
        verbose_name = 'Galeri Kategorisi'
        verbose_name_plural = 'Galeri Kategorileri'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('gallery:category_detail', args=[self.slug])

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name='Başlık')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    image = models.ImageField(upload_to='gallery/images/', verbose_name='Görsel')
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images', verbose_name='Kategori')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='Yükleme Tarihi')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    order = models.PositiveIntegerField(default=0, verbose_name='Gösterim Sırası')
    
    class Meta:
        verbose_name = 'Galeri Görseli'
        verbose_name_plural = 'Galeri Görselleri'
        ordering = ['order', '-upload_date']
    
    def __str__(self):
        return self.title