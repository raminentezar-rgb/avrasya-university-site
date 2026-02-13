from django.db import models
from django.urls import reverse
import os


class AdayMenu(models.Model):
    title = models.CharField(max_length=255, verbose_name="Menü Başlığı")
    icon = models.CharField(max_length=50, verbose_name="Icon Sınıfı")
    description = models.TextField(verbose_name="Açıklama")
    link = models.CharField(max_length=255, verbose_name="Link")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    
    class Meta:
        verbose_name = "Aday Menü"
        verbose_name_plural = "Aday Menüler"
        ordering = ['order']
    
    def __str__(self):
        return self.title

class AdaySayfa(models.Model):
    title = models.CharField(max_length=255, verbose_name="Sayfa Başlığı")
    slug = models.SlugField(unique=True, verbose_name="SEO URL")
    content = models.TextField(verbose_name="İçerik")
    image = models.ImageField(upload_to='aday/', blank=True, verbose_name="Görsel")
    is_published = models.BooleanField(default=True, verbose_name="Yayında")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # فایل‌های قابل دانلود
    pdf_file = models.FileField(
        upload_to='aday/pdf/',
        blank=True,
        null=True,
        verbose_name="PDF Dosyası"
    )
    word_file = models.FileField(
        upload_to='aday/word/',
        blank=True,
        null=True,
        verbose_name="Word Dosyası"
    )
    excel_file = models.FileField(
        upload_to='aday/excel/',
        blank=True,
        null=True,
        verbose_name="Excel Dosyası"
    )
    other_file = models.FileField(
        upload_to='aday/files/',
        blank=True,
        null=True,
        verbose_name="Diğer Dosya"
    )
    
    class Meta:
        verbose_name = "Aday Sayfa"
        verbose_name_plural = "Aday Sayfalar"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('aday_ogrenci:sayfa_detay', args=[self.slug])
    
    def get_filename(self, field_name):
        """اسم فایل را بدون مسیر برمی‌گرداند"""
        file_field = getattr(self, field_name)
        if file_field:
            return os.path.basename(file_field.name)
        return None
    
    def has_downloadable_files(self):
        """بررسی می‌کند که آیا فایل قابل دانلود وجود دارد یا نه"""
        return any([
            self.pdf_file,
            self.word_file,
            self.excel_file,
            self.other_file
        ])
class AdaySlider(models.Model):
    title = models.CharField(max_length=255, verbose_name="Başlık")
    image = models.ImageField(upload_to='aday/slider/', verbose_name="Slider Görseli")
    subtitle = models.CharField(max_length=500, blank=True, verbose_name="Alt Başlık")
    button_text = models.CharField(max_length=50, blank=True, verbose_name="Buton Yazısı")
    button_link = models.URLField(blank=True, verbose_name="Buton Linki")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    
    class Meta:
        verbose_name = "Aday Slider"
        verbose_name_plural = "Aday Sliderlar"
        ordering = ['order']
    
    def __str__(self):
        return self.title

class AdayIletisim(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    message = models.TextField(verbose_name="Mesaj")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="Okundu")
    
    class Meta:
        verbose_name = "Aday İletişim"
        verbose_name_plural = "Aday İletişimleri"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d.%m.%Y')}"