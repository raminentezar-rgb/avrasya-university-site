from django.db import models
from django.urls import reverse

# ابتدا ثابت‌ها را تعریف می‌کنیم
FAKULTE_CHOICES = [
    ('LEE', 'LEE'),
    ('FEF', 'FEF'),
    ('IIBF', 'IIBF'),
    ('MMF', 'MMF'),
    ('SBF', 'SBF'),
    ('ILTF', 'ILTF'),
    ('SPOR', 'SPOR'),
    ('UBY', 'UBY'),
    ('MYO', 'MYO'),
    ('SHMYO', 'SHMYO'),
    ('GENEL', 'Genel Duyuru'),
]

class Bolum(models.Model):
    """مدل جدید برای ذخیره رشته‌های تحصیلی"""
    ad = models.CharField(max_length=255, verbose_name="Bölüm Adı")
    kod = models.SlugField(unique=True, verbose_name="Bölüm Kodu")
    fakulte = models.CharField(
        max_length=10,
        choices=FAKULTE_CHOICES,
        verbose_name="Bağlı Fakülte"
    )
    aciklama = models.TextField(blank=True, verbose_name="Açıklama")
    aktif = models.BooleanField(default=True, verbose_name="Aktif")
    
    class Meta:
        verbose_name = "Bölüm"
        verbose_name_plural = "Bölümler"
        ordering = ['fakulte', 'ad']
    
    def __str__(self):
        return f"{self.ad} - {self.get_fakulte_display()}"

class Duyuru(models.Model):
    FAKULTE_CHOICES = FAKULTE_CHOICES
    
    baslik = models.CharField(max_length=255, verbose_name="Başlık")
    slug = models.SlugField(unique=True, verbose_name="SEO URL")
    ozet = models.TextField(blank=True, verbose_name="Özet")
    icerik = models.TextField(verbose_name="İçerik")
    yayin_tarihi = models.DateTimeField(verbose_name="Yayın Tarihi")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    yayinda = models.BooleanField(default=False, verbose_name="Yayında")
    fakulte = models.CharField(
        max_length=10,
        choices=FAKULTE_CHOICES,
        default='GENEL',
        verbose_name="Fakülte/Bölüm"
    )
    # فیلد جدید برای انتخاب رشته‌ها
    bolumler = models.ManyToManyField(
        Bolum,
        blank=True,
        verbose_name="İlgili Bölümler",
        help_text="Bu duyurunun gösterileceği bölümleri seçin"
    )

    class Meta:
        ordering = ['-yayin_tarihi']
        verbose_name = "Duyuru"
        verbose_name_plural = "Duyurular"
        indexes = [
            models.Index(fields=['fakulte', 'yayinda', 'yayin_tarihi']),
        ]

    def __str__(self):
        return f"{self.baslik} - {self.get_fakulte_display()}"

    def get_absolute_url(self):
        return reverse('duyurular:detay', args=[self.slug])

    def mevcut_dosyalar(self):
        """Mevcut dosyaları liste olarak döndürür"""
        dosyalar = []
        for dosya in self.dosyalar.all():
            dosyalar.append({
                'adi': dosya.dosya_adi,
                'url': dosya.dosya.url,
                'icon': dosya.get_icon(),
                'tur': dosya.get_tur_display(),
                'aciklama': dosya.aciklama
            })
        return dosyalar

    def get_fakulte_adi(self):
        """نام کامل دانشکده را برمی‌گرداند"""
        fakulte_adlari = {
            'LEE': 'Lisansüstü Eğitim Enstitüsü',
            'FEF': 'Fen-Edebiyat Fakültesi',
            'IIBF': 'İktisadi ve İdari Bilimler Fakültesi',
            'MMF': 'Mühendislik-Mimarlık Fakültesi',
            'SBF': 'Sağlık Bilimleri Fakültesi',
            'ILTF': 'İlahiyat Fakültesi',
            'SPOR': 'Spor Bilimleri Fakültesi',
            'UBY': 'Uygulamalı Bilimler Yüksekokulu',
            'MYO': 'Meslek Yüksekokulu',
            'SHMYO': 'Sağlık Hizmetleri Meslek Yüksekokulu',
            'GENEL': 'Genel Duyurular'
        }
        return fakulte_adlari.get(self.fakulte, self.get_fakulte_display())

    def get_bolum_adlari(self):
        """نام رشته‌های مرتبط را برمی‌گرداند"""
        return ", ".join([bolum.ad for bolum in self.bolumler.all()])


class DuyuruDosya(models.Model):
    DOSYA_TURleri = [
        ('word', 'Word Belgesi'),
        ('pdf', 'PDF Belgesi'),
        ('excel', 'Excel Dosyası'),
        ('resim', 'Resim'),
        ('arsiv', 'Arşiv Dosyası'),
        ('diger', 'Diğer'),
    ]
    
    duyuru = models.ForeignKey(
        Duyuru, 
        on_delete=models.CASCADE, 
        related_name='dosyalar',
        verbose_name="Duyuru"
    )
    dosya = models.FileField(
        upload_to='duyurular/dosyalar/%Y/%m/%d/',
        verbose_name="Dosya"
    )
    dosya_adi = models.CharField(
        max_length=255,
        verbose_name="Dosya Adı",
        blank=True
    )
    tur = models.CharField(
        max_length=10,
        choices=DOSYA_TURleri,
        default='diger',
        verbose_name="Dosya Türü"
    )
    aciklama = models.TextField(
        blank=True,
        verbose_name="Açıklama"
    )
    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )

    class Meta:
        verbose_name = "Duyuru Dosyası"
        verbose_name_plural = "Duyuru Dosyaları"
        ordering = ['tur', 'dosya_adi']

    def __str__(self):
        return self.dosya_adi or self.dosya.name

    def get_icon(self):
        """Dosya türüne göre ikon belirleme"""
        icon_map = {
            'word': 'bi-file-word',
            'pdf': 'bi-file-pdf',
            'excel': 'bi-file-excel',
            'resim': 'bi-file-image',
            'arsiv': 'bi-file-zip',
            'diger': 'bi-file-earmark'
        }
        return icon_map.get(self.tur, 'bi-file-earmark')

    def save(self, *args, **kwargs):
        # Dosya adını otomatik olarak ayarla
        if not self.dosya_adi:
            self.dosya_adi = self.dosya.name
        super().save(*args, **kwargs)