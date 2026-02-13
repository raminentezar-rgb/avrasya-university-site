# meslek_yuksekokulu/models.py
from django.db import models
from django.urls import reverse
from duyurular.models import Duyuru, DuyuruDosya

class MeslekYuksekokuluDuyuru(models.Model):
    ana_duyuru = models.OneToOneField(
        Duyuru, 
        on_delete=models.CASCADE,
        related_name='meslek_yuksekokulu_duyuru',
        verbose_name="Ana Duyuru",
        null=True,
        blank=True
    )
    
    KATEGORI_CHOICES = [
        ('akademik', 'Akademik'),
        ('etkinlik', 'Etkinlik'),
        ('ogrenci', 'Öğrenci'),
        ('genel', 'Genel'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    icerik = models.TextField(verbose_name="İçerik")
    ozet = models.TextField(blank=True, verbose_name="Özet", help_text="Kısa özet (opsiyonel)")
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='genel', verbose_name="Kategori")
    
    dosya = models.FileField(upload_to='meslek_yuksekokulu/duyurular/', blank=True, null=True, verbose_name="Dosya Eki")
    
    yayin_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Yayın Tarihi")
    guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    yayinda = models.BooleanField(default=True, verbose_name="Yayında")
    onemli = models.BooleanField(default=False, verbose_name="Önemli Duyuru")
    
    sira = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    
    class Meta:
        verbose_name = "Meslek Yüksekokulu Duyurusu"
        verbose_name_plural = "Meslek Yüksekokulu Duyuruları"
        ordering = ['-onemli', '-yayin_tarihi', 'sira']
    
    def __str__(self):
        return self.baslik
    
    def get_absolute_url(self):
        return reverse('meslek_yuksekokulu:duyuru_detay', args=[self.id])
    
    @property
    def kisa_ozet(self):
        if self.ozet:
            return self.ozet[:100] + "..." if len(self.ozet) > 100 else self.ozet
        return self.icerik[:100] + "..." if len(self.icerik) > 100 else self.icerik
    
    @property
    def dosya_adi(self):
        if self.dosya:
            return self.dosya.name.split('/')[-1]
        return None

    def mevcut_dosyalar(self):
        dosyalar = []
        if self.ana_duyuru:
            for dosya in self.ana_duyuru.dosyalar.all():
                dosyalar.append({
                    'adi': dosya.dosya_adi,
                    'url': dosya.dosya.url,
                    'icon': dosya.get_icon(),
                    'tur': dosya.get_tur_display(),
                    'aciklama': dosya.aciklama
                })
        return dosyalar

    def save(self, *args, **kwargs):
        if self.ana_duyuru:
            self.baslik = self.ana_duyuru.baslik
            self.icerik = self.ana_duyuru.icerik
            self.ozet = self.ana_duyuru.ozet
            self.yayin_tarihi = self.ana_duyuru.yayin_tarihi
            self.yayinda = self.ana_duyuru.yayinda
        super().save(*args, **kwargs)


class MeslekYuksekokuluDosya(models.Model):
    DOSYA_TURleri = [
        ('word', 'Word Belgesi'),
        ('pdf', 'PDF Belgesi'),
        ('excel', 'Excel Dosyası'),
        ('resim', 'Resim'),
        ('arsiv', 'Arşiv Dosyası'),
        ('diger', 'Diğer'),
    ]
    
    duyuru = models.ForeignKey(
        MeslekYuksekokuluDuyuru, 
        on_delete=models.CASCADE, 
        related_name='dosyalar',
        verbose_name="Duyuru"
    )
    dosya = models.FileField(
        upload_to='meslek_yuksekokulu/dosyalar/%Y/%m/%d/',
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
        verbose_name = "Meslek Yüksekokulu Dosyası"
        verbose_name_plural = "Meslek Yüksekokulu Dosyaları"
        ordering = ['tur', 'dosya_adi']

    def __str__(self):
        return self.dosya_adi or self.dosya.name

    def get_icon(self):
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
        if not self.dosya_adi:
            self.dosya_adi = self.dosya.name
        super().save(*args, **kwargs)