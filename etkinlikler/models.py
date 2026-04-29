from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
import sys

class Etkinlik(models.Model):
    ETKINLIK_TURU_CHOICES = [
        ('konferans', 'Konferans / Kongre / Sempozyum'),
        ('seminer', 'Seminer / Panel'),
        ('kultur', 'Kültür-Sanat Etkinliği'),
        ('spor', 'Spor Etkinliği'),
        ('tanitim', 'Tanıtım Günleri'),
        ('workshop', 'Workshop / Atölye'),
        ('diger', 'Diğer'),
    ]
    
    baslik = models.CharField(max_length=255, verbose_name="Etkinlik Başlığı")
    slug = models.SlugField(unique=True, verbose_name="SEO URL")
    kisa_aciklama = models.TextField(blank=True, verbose_name="Kısa Açıklama")
    detayli_aciklama = models.TextField(verbose_name="Detaylı Açıklama")
    etkinlik_turu = models.CharField(
        max_length=20, 
        choices=ETKINLIK_TURU_CHOICES, 
        default='diger',
        verbose_name="Etkinlik Türü"
    )
    
    baslangic_tarihi = models.DateTimeField(verbose_name="Başlangıç Tarihi")
    bitis_tarihi = models.DateTimeField(verbose_name="Bitiş Tarihi", blank=True, null=True)
    yer = models.CharField(max_length=255, verbose_name="Etkinlik Yeri")
    
    afis = models.ImageField(
        upload_to='etkinlikler/afis/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name="Etkinlik Afişi",
        help_text="Önerilen boyut: Genişlik maksimum 1200px, yükseklik serbest. Posterin tamamı görünecektir."
    )
    
    katilim_linki = models.URLField(blank=True, verbose_name="Katılım Linki")
    kayit_gerekiyor = models.BooleanField(default=False, verbose_name="Kayıt Gerekiyor")
    ucretli = models.BooleanField(default=False, verbose_name="Ücretli Etkinlik")
    
    yayinda = models.BooleanField(default=False, verbose_name="Yayında")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['baslangic_tarihi']
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse('etkinlikler:detay', args=[self.slug])

    def yaklasan_etkinlik(self):
        """Etkinliğin yaklaşıp yaklaşmadığını kontrol eder"""
        return self.baslangic_tarihi <= timezone.now() + timezone.timedelta(days=7)

    def devam_ediyor(self):
        """Etkinliğin devam edip etmediğini kontrol eder"""
        now = timezone.now()
        if self.bitis_tarihi:
            return self.baslangic_tarihi <= now <= self.bitis_tarihi
        return self.baslangic_tarihi.date() == now.date()

    def gun_kaldi(self):
        """Etkinliğe kaç gün kaldığını hesaplar"""
        kalan_gun = (self.baslangic_tarihi.date() - timezone.now().date()).days
        return max(0, kalan_gun)

    def optimize_afis(self):
        """Afiş görselini optimize eder - boyutlandırır ve sıkıştırır"""
        if not self.afis:
            return
        
        # Dosya yolunu al
        img_path = self.afis.path
        
        # Dosya mevcut mu kontrol et
        if not os.path.exists(img_path):
            return
        
        try:
            # Görseli aç
            img = Image.open(img_path)
            
            # RGB formatına çevir (şeffaflık sorunları için)
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Maksimum genişlik 1200px, yükseklik otomatik orantılı
            max_width = 1200
            if img.width > max_width:
                oran = max_width / img.width
                yeni_yukseklik = int(img.height * oran)
                img = img.resize((max_width, yeni_yukseklik), Image.LANCZOS)
            
            # Görseli kaydet (kalite: 85, optimize et)
            img.save(img_path, 'JPEG', quality=85, optimize=True)
            
        except Exception as e:
            # Hata durumunda logla ama kaydetmeyi engelleme
            print(f"Afiş optimize edilirken hata: {e}")

    def save(self, *args, **kwargs):
        """Kaydetme işlemi - afişi optimize et"""
        # Önce normal kaydet
        super().save(*args, **kwargs)
        
        # Kaydettikten sonra afişi optimize et
        self.optimize_afis()