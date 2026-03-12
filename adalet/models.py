# app_name: adalet/models.py

from django.db import models
from duyurular.models import Duyuru
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class AdaletDuyuruManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            bolumler__kod='adalet',
            yayinda=True
        )

class AdaletDuyuru(Duyuru):
    """مدل پروکسی برای نمایش اطلاعیه‌های رشته حقوق و عدالت کیفری"""
    
    objects = AdaletDuyuruManager()
    
    class Meta:
        proxy = True
        verbose_name = _("Adalet Duyurusu")
        verbose_name_plural = _("Adalet Duyuruları")

class AdaletEtkinlik(models.Model):
    ETKINLIK_TURU_CHOICES = [
        ('konferans', _('Konferans / Kongre / Sempozyum')),
        ('seminer', _('Seminer / Panel')),
        ('kultur', _('Kültür-Sanat Etkinliği')),
        ('spor', _('Spor Etkinliği')),
        ('tanitim', _('Tanıtım Günleri')),
        ('workshop', _('Workshop / Atölye')),
        ('sergi', _('Sergi')),
        ('yarisma', _('Yarışma')),
        ('diger', _('Diğer')),
    ]
    
    baslik = models.CharField(max_length=255, verbose_name=_("Etkinlik Başlığı"))
    slug = models.SlugField(unique=True, verbose_name=_("SEO URL"))
    kisa_aciklama = models.TextField(blank=True, verbose_name=_("Kısa Açıklama"))
    detayli_aciklama = models.TextField(verbose_name=_("Detaylı Açıklama"))
    etkinlik_turu = models.CharField(
        max_length=20, 
        choices=ETKINLIK_TURU_CHOICES, 
        default='diger',
        verbose_name=_("Etkinlik Türü")
    )
    
    baslangic_tarihi = models.DateTimeField(verbose_name=_("Başlangıç Tarihi"))
    bitis_tarihi = models.DateTimeField(verbose_name=_("Bitiş Tarihi"), blank=True, null=True)
    yer = models.CharField(max_length=255, verbose_name=_("Etkinlik Yeri"))
    
    afis = models.ImageField(
        upload_to='etkinlikler/afis/adalet/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name=_("Etkinlik Afişi")
    )
    
    katilim_linki = models.URLField(blank=True, verbose_name=_("Katılım Linki"))
    kayit_gerekiyor = models.BooleanField(default=False, verbose_name=_("Kayıت Gerekiyor"))
    ucretli = models.BooleanField(default=False, verbose_name=_("Ücretli Etkinlik"))
    
    yayinda = models.BooleanField(default=False, verbose_name=_("Yayında"))
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['baslangic_tarihi']
        verbose_name = _("Etkinlik (Adalet)")
        verbose_name_plural = _("Etkinlikler (Adalet)")

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse('adalet:etkinlik_detay', args=[self.slug])

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

class AdaletDersProgrami(models.Model):
    SINIF_CHOICES = [
        ('1', _('1. Sınıf')),
        ('2', _('2. Sınıf')),
        ('3', _('3. Sınıf')),
        ('4', _('4. Sınıf')),
        ('tum', _('Tüm Sınıflar')),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name=_("Başlık"))
    aciklama = models.TextField(blank=True, verbose_name=_("Açıklama"))
    dosya = models.FileField(upload_to='ders_programlari/adalet/', verbose_name=_("Dosya"))
    sinif = models.CharField(max_length=10, choices=SINIF_CHOICES, verbose_name=_("Sınıf"))
    yayin_tarihi = models.DateTimeField(default=timezone.now, verbose_name=_("Yayın Tarihi"))
    aktif = models.BooleanField(default=True, verbose_name=_("Aktif"))
    
    class Meta:
        verbose_name = _("Ders Programı (Adalet)")
        verbose_name_plural = _("Ders Programları (Adalet)")
        ordering = ['-yayin_tarihi']
    
    def __str__(self):
        return f"{self.baslik} - {self.get_sinif_display()}"