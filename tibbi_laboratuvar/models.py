# app_name: tibbi_laboratuvar/models.py

from django.db import models
from duyurular.models import Duyuru
from django.urls import reverse
from django.utils import timezone

class TibbiLaboratuvarDuyuruManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            bolumler__kod='tibbi_laboratuvar',
            yayinda=True
        )

class TibbiLaboratuvarDuyuru(Duyuru):
    """مدل پروکسی برای نمایش اطلاعیه‌های رشته پزشکی آزمایشگاهی"""
    
    objects = TibbiLaboratuvarDuyuruManager()
    
    class Meta:
        proxy = True
        verbose_name = "Tıbbi Laboratuvar Duyurusu"
        verbose_name_plural = "Tıbbi Laboratuvar Duyuruları"

class TibbiLaboratuvarEtkinlik(models.Model):
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
        upload_to='etkinlikler/afis/tibbi_laboratuvar/%Y/%m/%d/', 
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
        verbose_name = "Etkinlik (Tıbbi Laboratuvar)"
        verbose_name_plural = "Etkinlikler (Tıbbi Laboratuvar)"

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse('tibbi_laboratuvar:etkinlik_detay', args=[self.slug])

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

class TibbiLaboratuvarDersProgrami(models.Model):
    SINIF_CHOICES = [
        ('1', '1. Sınıf'),
        ('2', '2. Sınıf'),
        ('3', '3. Sınıf'),
        ('4', '4. Sınıf'),
        ('tum', 'Tüm Sınıflar'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    aciklama = models.TextField(blank=True, verbose_name="Açıklama")
    dosya = models.FileField(upload_to='ders_programlari/tibbi_laboratuvar/', verbose_name="Dosya")
    sinif = models.CharField(max_length=10, choices=SINIF_CHOICES, verbose_name="Sınıf")
    yayin_tarihi = models.DateTimeField(default=timezone.now, verbose_name="Yayın Tarihi")
    aktif = models.BooleanField(default=True, verbose_name="Aktif")
    
    class Meta:
        verbose_name = "Ders Programı (Tıbbi Laboratuvar)"
        verbose_name_plural = "Ders Programları (Tıbbi Laboratuvar)"
        ordering = ['-yayin_tarihi']
    
    def __str__(self):
        return f"{self.baslik} - {self.get_sinif_display()}"

class TibbiLaboratuvarFaaliyetGrubu(models.Model):
    TUR_CHOICES = [
        ('idari', 'İdari Faaliyetler'),
        ('diger', 'Diğer Faaliyetler'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name="Grup Başlığı (Örn: İdari Faaliyetler 2023-2024)")
    faaliyet_turu = models.CharField(max_length=10, choices=TUR_CHOICES, verbose_name="Faaliyet Türü")
    sira = models.IntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "Faaliyet Grubu (Tibbi Laboratuvar)"
        verbose_name_plural = "Faaliyet Grupları (Tibbi Laboratuvar)"
        ordering = ['sira', '-id']
        
    def __str__(self):
        return f"{self.baslik} ({self.get_faaliyet_turu_display()})"

class TibbiLaboratuvarFaaliyet(models.Model):
    grup = models.ForeignKey(TibbiLaboratuvarFaaliyetGrubu, on_delete=models.CASCADE, related_name='faaliyetler', verbose_name="Faaliyet Grubu")
    baslik = models.CharField(max_length=300, verbose_name="Faaliyet Başlığı")
    tarih = models.CharField(max_length=100, blank=True, verbose_name="Tarih / Dönem")
    icerik = models.TextField(blank=True, verbose_name="İçerik")
    sira = models.IntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "Faaliyet (Tibbi Laboratuvar)"
        verbose_name_plural = "Faaliyetler (Tibbi Laboratuvar)"
        ordering = ['sira', '-id']
        
    def __str__(self):
        return self.baslik

class TibbiLaboratuvarFaaliyetGorseli(models.Model):
    faaliyet = models.ForeignKey(TibbiLaboratuvarFaaliyet, on_delete=models.CASCADE, related_name='gorseller', verbose_name="Faaliyet")
    gorsel = models.ImageField(upload_to=f'faaliyetler/tibbi_laboratuvar/', verbose_name="Görsel")
    sira = models.IntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "Faaliyet Görseli (Tibbi Laboratuvar)"
        verbose_name_plural = "Faaliyet Görselleri (Tibbi Laboratuvar)"
        ordering = ['sira', 'id']
        
    def __str__(self):
        return f"{self.faaliyet.baslik} - Görsel {self.id}"
