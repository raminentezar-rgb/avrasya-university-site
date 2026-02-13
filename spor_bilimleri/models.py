# spor_bilimleri/models.py
from django.db import models
from django.urls import reverse
from duyurular.models import Duyuru

class SporBilimleriDuyuru(models.Model):
    # لینک به اطلاعیه اصلی
    ana_duyuru = models.OneToOneField(
        Duyuru, 
        on_delete=models.CASCADE,
        related_name='spor_bilimleri_duyuru',
        verbose_name="Ana Duyuru",
        null=True,
        blank=True
    )
    
    KATEGORI_CHOICES = [
        ('akademik', 'Akademik'),
        ('etkinlik', 'Etkinlik'),
        ('ogrenci', 'Öğrenci'),
        ('antrenman', 'Antrenman'),
        ('yarisma', 'Yarışma'),
        ('tesis', 'Tesis'),
        ('kultur', 'Spor Kültürü'),
        ('saglik', 'Spor Sağlığı'),
        ('mezun', 'Mezun'),
        ('genel', 'Genel'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    icerik = models.TextField(verbose_name="İçerik")
    ozet = models.TextField(blank=True, verbose_name="Özet", help_text="Kısa özet (opsiyonel)")
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='genel', verbose_name="Kategori")
    
    # فایل‌های ضمیمه
    dosya = models.FileField(upload_to='spor_bilimleri/duyurular/', blank=True, null=True, verbose_name="Dosya Eki")
    
    # تاریخ‌ها
    yayin_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Yayın Tarihi")
    guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    # وضعیت
    yayinda = models.BooleanField(default=True, verbose_name="Yayında")
    onemli = models.BooleanField(default=False, verbose_name="Önemli Duyuru")
    
    # ترتیب نمایش
    sira = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    
    class Meta:
        verbose_name = "Spor Bilimleri Duyurusu"
        verbose_name_plural = "Spor Bilimleri Duyuruları"
        ordering = ['-onemli', '-yayin_tarihi', 'sira']
    
    def __str__(self):
        return self.baslik
    
    def get_absolute_url(self):
        return reverse('spor_bilimleri:duyuru_detay', args=[self.id])
    
    @property
    def kisa_ozet(self):
        """برگرداندن خلاصه کوتاه"""
        if self.ozet:
            return self.ozet[:100] + "..." if len(self.ozet) > 100 else self.ozet
        return self.icerik[:100] + "..." if len(self.icerik) > 100 else self.icerik
    
    @property
    def dosya_adi(self):
        """برگرداندن نام فایل"""
        if self.dosya:
            return self.dosya.name.split('/')[-1]
        return None

    def mevcut_dosyalar(self):
        """برگرداندن فایل‌های ضمیمه از اطلاعیه اصلی"""
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
        # اگر لینک به اطلاعیه اصلی وجود دارد، اطلاعات را همگام‌سازی کن
        if self.ana_duyuru:
            self.baslik = self.ana_duyuru.baslik
            self.icerik = self.ana_duyuru.icerik
            self.ozet = self.ana_duyuru.ozet
            self.yayin_tarihi = self.ana_duyuru.yayin_tarihi
            self.yayinda = self.ana_duyuru.yayinda
        super().save(*args, **kwargs)