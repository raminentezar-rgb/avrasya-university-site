# app_name: harita_muhendisligi/models.py

from django.db import models
from duyurular.models import Duyuru
from django.urls import reverse
from django.utils import timezone


class HaritaMuhendisligiDuyuruManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            bolumler__kod='harita_muhendisligi',
            yayinda=True
        )


class HaritaMuhendisligiDuyuru(Duyuru):
    """Proxy model for Harita Mühendisliği announcements"""
    
    objects = HaritaMuhendisligiDuyuruManager()
    
    class Meta:
        proxy = True
        verbose_name = "Harita Mühendisliği Duyurusu"
        verbose_name_plural = "Harita Mühendisliği Duyuruları"


class HaritaMuhendisligiEtkinlik(models.Model):
    ETKINLIK_TURU_CHOICES = [
        ('konferans', 'Konferans / Kongre / Sempozyum'),
        ('seminer', 'Seminer / Panel'),
        ('kultur', 'Kültür-Sanat Etkinliği'),
        ('spor', 'Spor Etkinliği'),
        ('tanitim', 'Tanıtım Günleri'),
        ('workshop', 'Workshop / Atölye'),
        ('sergi', 'Sergi'),
        ('yarisma', 'Yarışma'),
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
        upload_to='etkinlikler/afis/harita_muhendisligi/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Etkinlik Afişi"
    )
    
    katilim_linki = models.URLField(blank=True, verbose_name="Katılım Linki")
    kayit_gerekiyor = models.BooleanField(default=False, verbose_name="Kayıt Gerekiyor")
    ucretli = models.BooleanField(default=False, verbose_name="Ücretli Etkinlik")
    
    yayinda = models.BooleanField(default=False, verbose_name="Yayında")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['baslangic_tarihi']
        verbose_name = "Etkinlik (Harita Mühendisliği)"
        verbose_name_plural = "Etkinlikler (Harita Mühendisliği)"

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse('harita_muhendisligi:etkinlik_detay', args=[self.slug])

    def yaklasan_etkinlik(self):
        """Checks if the event is approaching"""
        return self.baslangic_tarihi <= timezone.now() + timezone.timedelta(days=7)

    def devam_ediyor(self):
        """Checks if the event is ongoing"""
        now = timezone.now()
        if self.bitis_tarihi:
            return self.baslangic_tarihi <= now <= self.bitis_tarihi
        return self.baslangic_tarihi.date() == now.date()

    def gun_kaldi(self):
        """Calculates days remaining until the event"""
        kalan_gun = (self.baslangic_tarihi.date() - timezone.now().date()).days
        return max(0, kalan_gun)


class HaritaMuhendisligiDersProgrami(models.Model):
    SINIF_CHOICES = [
        ('1', '1. Sınıf'),
        ('2', '2. Sınıf'),
        ('3', '3. Sınıf'),
        ('4', '4. Sınıf'),
        ('tum', 'Tüm Sınıflar'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    aciklama = models.TextField(blank=True, verbose_name="Açıklama")
    dosya = models.FileField(upload_to='ders_programlari/harita_muhendisligi/', verbose_name="Dosya")
    sinif = models.CharField(max_length=10, choices=SINIF_CHOICES, verbose_name="Sınıf")
    yayin_tarihi = models.DateTimeField(default=timezone.now, verbose_name="Yayın Tarihi")
    aktif = models.BooleanField(default=True, verbose_name="Aktif")
    
    class Meta:
        verbose_name = "Ders Programı (Harita Mühendisliği)"
        verbose_name_plural = "Ders Programları (Harita Mühendisliği)"
        ordering = ['-yayin_tarihi']
    
    def __str__(self):
        return f"{self.baslik} - {self.get_sinif_display()}"