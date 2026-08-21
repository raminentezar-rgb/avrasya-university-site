# app_name: odyometri/models.py

from django.db import models
from duyurular.models import Duyuru
from django.urls import reverse
from django.utils import timezone

class OdyometriDuyuruManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            bolumler__kod='odyometri',
            yayinda=True
        )

class OdyometriDuyuru(Duyuru):
    """مدل پروکسی برای نمایش اطلاعیه‌های رشته ادیومتری"""
    
    objects = OdyometriDuyuruManager()
    
    class Meta:
        proxy = True
        verbose_name = "Odyometri Duyurusu"
        verbose_name_plural = "Odyometri Duyuruları"

class OdyometriEtkinlik(models.Model):
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
        upload_to='etkinlikler/afis/odyometri/%Y/%m/%d/', 
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
        verbose_name = "Etkinlik (Odyometri)"
        verbose_name_plural = "Etkinlikler (Odyometri)"

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse('odyometri:etkinlik_detay', args=[self.slug])

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

class OdyometriDersProgrami(models.Model):
    SINIF_CHOICES = [
        ('1', '1. Sınıf'),
        ('2', '2. Sınıf'),
        ('3', '3. Sınıf'),
        ('4', '4. Sınıf'),
        ('tum', 'Tüm Sınıflar'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    aciklama = models.TextField(blank=True, verbose_name="Açıklama")
    dosya = models.FileField(upload_to='ders_programlari/odyometri/', verbose_name="Dosya")
    sinif = models.CharField(max_length=10, choices=SINIF_CHOICES, verbose_name="Sınıf")
    yayin_tarihi = models.DateTimeField(default=timezone.now, verbose_name="Yayın Tarihi")
    aktif = models.BooleanField(default=True, verbose_name="Aktif")
    
    class Meta:
        verbose_name = "Ders Programı (Odyometri)"
        verbose_name_plural = "Ders Programları (Odyometri)"
        ordering = ['-yayin_tarihi']
    
    def __str__(self):
        return f"{self.baslik} - {self.get_sinif_display()}"

class OdyometriFaaliyetGrubu(models.Model):
    TUR_CHOICES = [
        ('idari', 'İdari Faaliyetler'),
        ('diger', 'Diğer Faaliyetler'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name="Grup Başlığı (Örn: İdari Faaliyetler 2023-2024)")
    faaliyet_turu = models.CharField(max_length=10, choices=TUR_CHOICES, verbose_name="Faaliyet Türü")
    sira = models.IntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "Faaliyet Grubu (Odyometri)"
        verbose_name_plural = "Faaliyet Grupları (Odyometri)"
        ordering = ['sira', '-id']
        
    def __str__(self):
        return f"{self.baslik} ({self.get_faaliyet_turu_display()})"

class OdyometriFaaliyet(models.Model):
    grup = models.ForeignKey(OdyometriFaaliyetGrubu, on_delete=models.CASCADE, related_name='faaliyetler', verbose_name="Faaliyet Grubu")
    baslik = models.CharField(max_length=300, verbose_name="Faaliyet Başlığı")
    tarih = models.CharField(max_length=100, blank=True, verbose_name="Tarih / Dönem")
    icerik = models.TextField(blank=True, verbose_name="İçerik")
    sira = models.IntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "Faaliyet (Odyometri)"
        verbose_name_plural = "Faaliyetler (Odyometri)"
        ordering = ['sira', '-id']
        
    def __str__(self):
        return self.baslik

class OdyometriFaaliyetGorseli(models.Model):
    faaliyet = models.ForeignKey(OdyometriFaaliyet, on_delete=models.CASCADE, related_name='gorseller', verbose_name="Faaliyet")
    gorsel = models.ImageField(upload_to=f'faaliyetler/odyometri/', verbose_name="Görsel")
    sira = models.IntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "Faaliyet Görseli (Odyometri)"
        verbose_name_plural = "Faaliyet Görselleri (Odyometri)"
        ordering = ['sira', 'id']
        
    def __str__(self):
        return f"{self.faaliyet.baslik} - Görsel {self.id}"
