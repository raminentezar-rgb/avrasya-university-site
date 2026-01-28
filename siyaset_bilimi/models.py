from django.db import models
from duyurular.models import Duyuru
from django.urls import reverse
from django.utils import timezone

class SiyasetBilimiDuyuruManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            bolumler__kod='siyaset-bilimi',
            yayinda=True
        )

class SiyasetBilimiDuyuru(Duyuru):
    """مدل پروکسی برای نمایش اطلاعیه‌های علوم سیاسی"""
    
    objects = SiyasetBilimiDuyuruManager()
    
    class Meta:
        proxy = True
        verbose_name = "Siyaset Bilimi Duyurusu"
        verbose_name_plural = "Siyaset Bilimi Duyuruları"

class SiyasetBilimi_Etkinlik(models.Model):
    ETKINLIK_TURU_CHOICES = [
        ('konferans', 'Konferans / Kongre / Sempozyum'),
        ('seminer', 'Seminer / Panel'),
        ('kultur', 'Kültür-Sanat Etkinliği'),
        ('spor', 'Spor Etkinliği'),
        ('tanitim', 'Tanıtım Günleri'),
        ('workshop', 'Workshop / Atölye'),
        ('proje', 'Proje Yarışması'),
        ('teknik_gezi', 'Teknik Gezi'),
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
        upload_to='etkinlikler/siyaset_bilimi/afis/%Y/%m/%d/', 
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
        verbose_name = "Siyaset Bilimi Etkinliği"
        verbose_name_plural = "Siyaset Bilimi Etkinlikleri"

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse('siyaset_bilimi:etkinlik_detay', args=[self.slug])

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

class DersProgramiDosyaSiyasetBilimi(models.Model):
    DOSYA_TURU_CHOICES = [
        ('pdf', 'PDF'),
        ('word', 'Word'),
        ('excel', 'Excel'),
        ('resim', 'Resim'),
        ('diger', 'Diğer'),
    ]
    
    SINIF_CHOICES = [
        ('1', '1. Sınıf'),
        ('2', '2. Sınıf'),
        ('3', '3. Sınıf'),
        ('4', '4. Sınıf'),
        ('tum', 'Tüm Sınıflar'),
        ('lisansustu', 'Lisansüstü'),
    ]
    
    baslik = models.CharField(max_length=255, verbose_name="Dosya Başlığı")
    aciklama = models.TextField(blank=True, verbose_name="Açıklama")
    dosya = models.FileField(
        upload_to='ders_programlari_siyaset_bilimi/%Y/%m/%d/',
        verbose_name="Dosya"
    )
    dosya_turu = models.CharField(
        max_length=10,
        choices=DOSYA_TURU_CHOICES,
        default='pdf',
        verbose_name="Dosya Türü"
    )
    sinif = models.CharField(
        max_length=15,
        choices=SINIF_CHOICES,
        default='1',
        verbose_name="Sınıf"
    )
    akademik_yil = models.CharField(
        max_length=9,
        default='2024-2025',
        verbose_name="Akademik Yıl"
    )
    yayin_tarihi = models.DateField(
        default=timezone.now,
        verbose_name="Yayın Tarihi"
    )
    sira = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıra"
    )
    aktif = models.BooleanField(
        default=True,
        verbose_name="Aktif"
    )
    
    class Meta:
        verbose_name = "Ders Programı Dosyası (Siyaset Bilimi)"
        verbose_name_plural = "Ders Programı Dosyaları (Siyaset Bilimi)"
        ordering = ['sira', '-yayin_tarihi']
    
    def __str__(self):
        return f"{self.baslik} - {self.akademik_yil}"
    
    def get_dosya_icon(self):
        """آیکون مناسب برای نوع فایل برمی‌گرداند"""
        icon_map = {
            'pdf': 'bi-file-earmark-pdf',
            'word': 'bi-file-earmark-word',
            'excel': 'bi-file-earmark-excel',
            'resim': 'bi-file-image',
            'diger': 'bi-file-earmark'
        }
        return icon_map.get(self.dosya_turu, 'bi-file-earmark')
    
    def get_dosya_boyutu(self):
        """سایز فایل را به فرمت خوانا برمی‌گرداند"""
        try:
            size = self.dosya.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        except:
            return "Bilinmiyor"