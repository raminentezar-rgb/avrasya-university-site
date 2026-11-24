from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import logging
import os
import secrets

logger = logging.getLogger(__name__)

ALLOWED_EVENT_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
ALLOWED_EVENT_FILE_EXTENSIONS = {
    '.pdf', '.xls', '.xlsx', '.xlsm', '.csv',
    '.doc', '.docx',
    '.jpg', '.jpeg', '.png', '.webp', '.gif',
}
MAX_EVENT_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25 MB per file


def validate_etkinlik_image(value):
    """Validate event gallery image extension and file size."""
    if not value:
        return
    ext = os.path.splitext(getattr(value, 'name', '') or '')[1].lower()
    if ext not in ALLOWED_EVENT_IMAGE_EXTENSIONS:
        raise ValidationError(
            'Geçersiz görsel formatı. Yalnızca JPG, JPEG, PNG, WEBP veya GIF yükleyebilirsiniz.'
        )
    if getattr(value, 'size', 0) > MAX_EVENT_ATTACHMENT_SIZE:
        raise ValidationError('Görsel boyutu en fazla 25 MB olabilir.')


def validate_etkinlik_file(value):
    """Validate event attachment extension (PDF, Excel, Word, or Image) and file size."""
    if not value:
        return
    ext = os.path.splitext(getattr(value, 'name', '') or '')[1].lower()
    if ext not in ALLOWED_EVENT_FILE_EXTENSIONS:
        raise ValidationError(
            'Geçersiz dosya formatı. Yalnızca PDF, Excel (.xls, .xlsx, .xlsm, .csv), Word veya görsel dosyaları yükleyebilirsiniz.'
        )
    if getattr(value, 'size', 0) > MAX_EVENT_ATTACHMENT_SIZE:
        raise ValidationError('Dosya boyutu en fazla 25 MB olabilir.')

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

    BIRIM_CHOICES = [
        ('GENEL', 'Üniversite Geneli'),
        ('REKTORLUK', 'Rektörlük / İdari Birimler'),
        ('KULUP', 'Öğrenci Kulüpleri'),
        ('MERKEZ', 'Araştırma / Uygulama Merkezleri'),
        ('LEE', 'Lisansüstü Eğitim Enstitüsü'),
        ('FEF', 'Fen-Edebiyat Fakültesi'),
        ('IIBF', 'İktisadi ve İdari Bilimler Fakültesi'),
        ('MMF', 'Mühendislik-Mimarlık Fakültesi'),
        ('SBF', 'Sağlık Bilimleri Fakültesi'),
        ('ILTF', 'İlahiyat Fakültesi'),
        ('SPOR', 'Spor Bilimleri Fakültesi'),
        ('UBY', 'Uygulamalı Bilimler Yüksekokulu'),
        ('MYO', 'Meslek Yüksekokulu'),
        ('SHMYO', 'Sağlık Hizmetleri Meslek Yüksekokulu'),
    ]
    
    baslik = models.CharField(max_length=255, verbose_name="Etkinlik Başlığı")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="SEO URL")
    kisa_aciklama = models.TextField(blank=True, verbose_name="Kısa Açıklama")
    detayli_aciklama = models.TextField(verbose_name="Detaylı Açıklama")
    etkinlik_turu = models.CharField(
        max_length=50, 
        choices=ETKINLIK_TURU_CHOICES, 
        default='diger',
        verbose_name="Etkinlik Türü"
    )
    fakulte = models.CharField(
        max_length=15,
        choices=BIRIM_CHOICES,
        blank=True,
        default='',
        verbose_name="Düzenleyen Birim / Fakülte"
    )
    duzenleyen = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Düzenleyen Kurum / Kulüp / Bölüm"
    )
    
    baslangic_tarihi = models.DateTimeField(verbose_name="Başlangıç Tarihi")
    bitis_tarihi = models.DateTimeField(verbose_name="Bitiş Tarihi", blank=True, null=True)
    yer = models.CharField(max_length=255, verbose_name="Etkinlik Yeri")
    harita_linki = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Harita / Konum Linki (Google Maps)"
    )
    
    afis = models.ImageField(
        max_length=500,
        upload_to='etkinlikler/afis/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name="Etkinlik Afişi",
        help_text="Önerilen boyut: Genişlik maksimum 1200px, yükseklik serbest. Posterin tamamı görünecektir."
    )
    
    katilim_linki = models.URLField(max_length=500, blank=True, verbose_name="Katılım Linki")
    kayit_gerekiyor = models.BooleanField(default=False, verbose_name="Kayıt Gerekiyor")
    kontenjan = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Kontenjan",
        help_text="Boş bırakılırsa kayıt kapasitesi sınırsız olur."
    )
    son_kayit_tarihi = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Son Kayıt Tarihi"
    )
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

    @property
    def aktif_kayit_sayisi(self) -> int:
        if hasattr(self, '_aktif_kayit_sayisi'):
            return int(self._aktif_kayit_sayisi or 0)
        return self.kayitlar.exclude(durum='iptal').count()

    @property
    def kalan_kontenjan(self):
        if self.kontenjan is None:
            return None
        return max(0, self.kontenjan - self.aktif_kayit_sayisi)

    @property
    def kayit_durumu(self):
        """Returns (is_open: bool, reason: str)."""
        if not self.yayinda or not self.kayit_gerekiyor:
            return False, 'Bu etkinlik için kayıt alınmamaktadır.'
        now = timezone.now()
        end_dt = self.bitis_tarihi or self.baslangic_tarihi
        if end_dt < now:
            return False, 'Etkinlik süresi tamamlanmıştır.'
        if self.son_kayit_tarihi and now > self.son_kayit_tarihi:
            return False, 'Son kayıt tarihi geçmiştir.'
        if self.kontenjan is not None and self.kalan_kontenjan <= 0:
            return False, 'Etkinlik kontenjanı dolmuştur.'
        return True, ''

    @property
    def kayit_acik_mi(self) -> bool:
        return self.kayit_durumu[0]

    @property
    def google_calendar_url(self) -> str:
        from urllib.parse import urlencode
        start_utc = timezone.localtime(self.baslangic_tarihi, timezone.UTC)
        end_dt = self.bitis_tarihi or (self.baslangic_tarihi + timezone.timedelta(hours=2))
        end_utc = timezone.localtime(end_dt, timezone.UTC)
        dates = f"{start_utc.strftime('%Y%m%dT%H%M%SZ')}/{end_utc.strftime('%Y%m%dT%H%M%SZ')}"
        details = (self.get_ozet or '')[:600]
        params = urlencode({
            'action': 'TEMPLATE',
            'text': self.baslik,
            'dates': dates,
            'details': details,
            'location': self.yer,
        })
        return f"https://calendar.google.com/calendar/render?{params}"

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

    def auto_generate_summaries(self):
        """
        Kısa Açıklama boş bırakıldığında veya Detaylı Açıklama ile birebir aynı yapıştırıldığında,
        Detaylı Açıklamadan otomatik olarak anlamlı ve profesyonel bir etkinlik özeti üretir.
        Modeltranslation'ın tüm dillerini (tr, en, fa, ar, ru, de) ve ana alanı destekler.
        """
        for lang in ['', '_tr', '_en', '_fa', '_ar', '_ru', '_de']:
            kisa_attr = f'kisa_aciklama{lang}'
            detay_attr = f'detayli_aciklama{lang}'
            
            if hasattr(self, kisa_attr) and hasattr(self, detay_attr):
                kisa_val = getattr(self, kisa_attr, None) or ''
                detay_val = getattr(self, detay_attr, None) or ''
                
                kisa_strip = kisa_val.strip()
                detay_strip = detay_val.strip()
                
                # Eğer detay dolu ama kısa açıklama boşsa VEYA ikisi de aynıysa (kullanıcı tüm metni kopyaladıysa)
                if detay_strip and (not kisa_strip or kisa_strip == detay_strip):
                    baslik_attr = f'baslik{lang}'
                    title_val = getattr(self, baslik_attr, '') or self.baslik or ''
                    summary = generate_event_summary(detay_strip, title=title_val)
                    if summary:
                        setattr(self, kisa_attr, summary)

    @property
    def get_ozet(self):
        """Kısa açıklama varsa döner, yoksa veya detayla aynıysa otomatik özet üretip döner."""
        kisa = (self.kisa_aciklama or '').strip()
        detay = (self.detayli_aciklama or '').strip()
        if kisa and kisa != detay:
            return kisa
        if detay:
            return generate_event_summary(detay, title=self.baslik)
        return ""

    def save(self, *args, **kwargs):
        """Kaydetme işlemi - özeti otomatik oluştur ve afişi optimize et"""
        # Detaylı açıklamadan otomatik özet üret
        self.auto_generate_summaries()
        
        # Normal kaydet
        super().save(*args, **kwargs)
        
        # Kaydettikten sonra afişi optimize et
        self.optimize_afis()


class EtkinlikGorsel(models.Model):
    """Bir etkinliğe ait sınırsız sayıda galeri görseli."""
    etkinlik = models.ForeignKey(
        Etkinlik,
        on_delete=models.CASCADE,
        related_name='gorseller',
        verbose_name="Etkinlik"
    )
    gorsel = models.ImageField(
        max_length=500,
        upload_to='etkinlikler/gorseller/%Y/%m/%d/',
        validators=[validate_etkinlik_image],
        verbose_name="Görsel"
    )
    baslik = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Görsel Başlığı / Açıklaması"
    )
    sira = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    class Meta:
        ordering = ['sira', 'olusturulma_tarihi']
        verbose_name = 'Etkinlik Görseli'
        verbose_name_plural = 'Etkinlik Görselleri'

    def __str__(self):
        return f"{self.display_title} - {self.etkinlik.baslik}"

    @property
    def display_title(self):
        if self.baslik:
            return self.baslik
        if self.gorsel and self.gorsel.name:
            return os.path.splitext(os.path.basename(self.gorsel.name))[0]
        return self.etkinlik.baslik

    def optimize_image(self):
        """Çok büyük galeri görsellerini güvenli şekilde yeniden boyutlandırır."""
        if not self.gorsel:
            return
        try:
            img_path = self.gorsel.path
        except (ValueError, NotImplementedError):
            return
        if not os.path.exists(img_path):
            return
        try:
            with Image.open(img_path) as img:
                max_width = 1600
                if img.width <= max_width:
                    return
                ratio = max_width / img.width
                resized = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
                ext = os.path.splitext(img_path)[1].lower()
                if ext in ('.jpg', '.jpeg') and resized.mode in ('RGBA', 'LA', 'P'):
                    resized = resized.convert('RGB')
                save_kwargs = {'optimize': True}
                if ext in ('.jpg', '.jpeg'):
                    save_kwargs['quality'] = 85
                resized.save(img_path, **save_kwargs)
        except Exception as exc:
            logger.warning("Etkinlik görseli optimize edilemedi (%s): %s", img_path, exc)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.optimize_image()


class EtkinlikDosya(models.Model):
    """Bir etkinliğe ait sınırsız sayıda PDF, Excel, Word veya ek görsel dosyası."""
    DOSYA_TUR_CHOICES = [
        ('pdf', 'PDF Belgesi'),
        ('excel', 'Excel Dosyası'),
        ('resim', 'Görsel'),
        ('word', 'Word Belgesi'),
        ('diger', 'Diğer'),
    ]

    etkinlik = models.ForeignKey(
        Etkinlik,
        on_delete=models.CASCADE,
        related_name='dosyalar',
        verbose_name="Etkinlik"
    )
    dosya = models.FileField(
        max_length=500,
        upload_to='etkinlikler/dosyalar/%Y/%m/%d/',
        validators=[validate_etkinlik_file],
        verbose_name="Dosya"
    )
    dosya_adi = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Dosya Başlığı"
    )
    dosya_turu = models.CharField(
        max_length=15,
        choices=DOSYA_TUR_CHOICES,
        blank=True,
        verbose_name="Dosya Türü"
    )
    aciklama = models.TextField(blank=True, verbose_name="Açıklama")
    sira = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    class Meta:
        ordering = ['sira', 'olusturulma_tarihi']
        verbose_name = 'Etkinlik Dosyası'
        verbose_name_plural = 'Etkinlik Dosyaları'

    def __str__(self):
        return f"{self.display_name} - {self.etkinlik.baslik}"

    @staticmethod
    def detect_file_type(filename: str) -> str:
        ext = os.path.splitext(filename or '')[1].lower()
        if ext == '.pdf':
            return 'pdf'
        if ext in ('.xls', '.xlsx', '.xlsm', '.csv'):
            return 'excel'
        if ext in ALLOWED_EVENT_IMAGE_EXTENSIONS:
            return 'resim'
        if ext in ('.doc', '.docx'):
            return 'word'
        return 'diger'

    @property
    def display_name(self) -> str:
        if self.dosya_adi:
            return self.dosya_adi
        if self.dosya and self.dosya.name:
            return os.path.basename(self.dosya.name)
        return "Dosya"

    @property
    def file_extension(self) -> str:
        if not self.dosya or not self.dosya.name:
            return ""
        return os.path.splitext(self.dosya.name)[1].lstrip('.').upper()

    @property
    def is_pdf(self) -> bool:
        return self.dosya_turu == 'pdf' or self.file_extension == 'PDF'

    @property
    def is_excel(self) -> bool:
        return self.dosya_turu == 'excel' or self.file_extension in ('XLS', 'XLSX', 'XLSM', 'CSV')

    @property
    def is_image(self) -> bool:
        ext = f".{self.file_extension.lower()}" if self.file_extension else ""
        return self.dosya_turu == 'resim' or ext in ALLOWED_EVENT_IMAGE_EXTENSIONS

    def get_icon(self) -> str:
        icons = {
            'pdf': 'fas fa-file-pdf',
            'excel': 'fas fa-file-excel',
            'resim': 'fas fa-file-image',
            'word': 'fas fa-file-word',
            'diger': 'fas fa-file-alt',
        }
        return icons.get(self.dosya_turu, 'fas fa-file-alt')

    def get_badge_color(self) -> str:
        colors = {
            'pdf': '#dc2626',
            'excel': '#15803d',
            'resim': '#1d61a9',
            'word': '#2563eb',
            'diger': '#475569',
        }
        return colors.get(self.dosya_turu, '#475569')

    def get_file_size(self) -> str:
        try:
            size = self.dosya.size
        except (OSError, ValueError):
            return "0 B"
        if size < 1024:
            return f"{size} B"
        if size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size / (1024 * 1024):.1f} MB"

    def save(self, *args, **kwargs):
        if self.dosya and self.dosya.name:
            if not self.dosya_turu:
                self.dosya_turu = self.detect_file_type(self.dosya.name)
            if not self.dosya_adi:
                base = os.path.splitext(os.path.basename(self.dosya.name))[0]
                self.dosya_adi = base[:255]
        elif not self.dosya_turu:
            self.dosya_turu = 'diger'
        super().save(*args, **kwargs)


class EtkinlikKonusmaci(models.Model):
    """Etkinlik konuşmacıları / eğitmenleri."""
    etkinlik = models.ForeignKey(
        Etkinlik,
        on_delete=models.CASCADE,
        related_name='konusmacilar',
        verbose_name="Etkinlik"
    )
    ad_soyad = models.CharField(max_length=150, verbose_name="Ad Soyad")
    unvan = models.CharField(max_length=150, blank=True, verbose_name="Unvan / Görev")
    kurum = models.CharField(max_length=200, blank=True, verbose_name="Kurum / Bölüm")
    fotograf = models.ImageField(
        max_length=500,
        upload_to='etkinlikler/konusmacilar/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[validate_etkinlik_image],
        verbose_name="Fotoğraf"
    )
    bio = models.TextField(blank=True, verbose_name="Konuşma Konusu / Kısa Özgeçmiş")
    sira = models.PositiveIntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        ordering = ['sira', 'id']
        verbose_name = 'Konuşmacı'
        verbose_name_plural = 'Konuşmacılar'

    def __str__(self):
        return f"{self.ad_soyad} - {self.etkinlik.baslik}"


class EtkinlikKayit(models.Model):
    """Etkinlik online katılımcı kayıtları."""
    DURUM_CHOICES = [
        ('onayli', 'Onaylı'),
        ('beklemede', 'Beklemede'),
        ('iptal', 'İptal'),
    ]

    etkinlik = models.ForeignKey(
        Etkinlik,
        on_delete=models.CASCADE,
        related_name='kayitlar',
        verbose_name="Etkinlik"
    )
    ad_soyad = models.CharField(max_length=150, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    telefon = models.CharField(max_length=30, verbose_name="Telefon")
    ogrenci_no = models.CharField(max_length=50, blank=True, verbose_name="Öğrenci No / T.C. No")
    kurum_fakulte = models.CharField(max_length=150, blank=True, verbose_name="Fakülte / Kurum")
    notlar = models.TextField(blank=True, verbose_name="Not / Soru")
    kayit_kodu = models.CharField(max_length=24, unique=True, blank=True, verbose_name="Kayıt Kodu")
    durum = models.CharField(max_length=15, choices=DURUM_CHOICES, default='onayli', verbose_name="Durum")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    class Meta:
        ordering = ['-olusturulma_tarihi']
        verbose_name = 'Etkinlik Kaydı'
        verbose_name_plural = 'Etkinlik Kayıtları'
        constraints = [
            models.UniqueConstraint(
                fields=['etkinlik', 'email'],
                condition=~Q(durum='iptal'),
                name='unique_active_etkinlik_email',
            )
        ]

    def __str__(self):
        return f"[{self.kayit_kodu}] {self.ad_soyad} - {self.etkinlik.baslik}"

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()
        if not self.kayit_kodu:
            year = timezone.now().year
            while True:
                code = f"ETK-{year}-{secrets.token_hex(3).upper()}"
                if not EtkinlikKayit.objects.filter(kayit_kodu=code).exists():
                    self.kayit_kodu = code
                    break
        super().save(*args, **kwargs)


class EtkinlikBildirimAboneligi(models.Model):
    """Yaklaşan ve yeni etkinlikler için e-posta bildirim aboneliği."""
    email = models.EmailField(unique=True, verbose_name="E-posta")
    ad_soyad = models.CharField(max_length=150, blank=True, verbose_name="Ad Soyad")
    tercih_turu = models.CharField(
        max_length=50,
        choices=[('', 'Tüm Etkinlikler')] + Etkinlik.ETKINLIK_TURU_CHOICES,
        blank=True,
        default='',
        verbose_name="Etkinlik Türü Tercihi"
    )
    aktif = models.BooleanField(default=True, verbose_name="Aktif")
    iptal_token = models.CharField(max_length=64, unique=True, blank=True, verbose_name="İptal Tokenı")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    class Meta:
        ordering = ['-olusturulma_tarihi']
        verbose_name = 'Etkinlik Bildirim Abonesi'
        verbose_name_plural = 'Etkinlik Bildirim Aboneleri'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()
        if not self.iptal_token:
            while True:
                tok = secrets.token_urlsafe(24)
                if not EtkinlikBildirimAboneligi.objects.filter(iptal_token=tok).exists():
                    self.iptal_token = tok
                    break
        super().save(*args, **kwargs)


def generate_event_summary(text, title='', max_chars=350):
    """
    Detaylı metinden otomatik, anlamlı ve temiz bir etkinlik özeti üretir.
    Gereksiz satırları, tarih/saat/yer tekrarlarını ve emojileri filtreler;
    etkinliğin ana konusunu ve amacını anlatan ilk 1-3 cümleyi seçer.
    """
    if not text:
        return ""
        
    import re
    from django.utils.html import strip_tags
    
    clean_text = strip_tags(text).replace('&nbsp;', ' ')
    
    meta_prefixes = (
        'tarih:', 'saat:', 'yer:', 'eğitmen:', 'konuşmacı:', 'egitmen:', 'konusmaci:',
        'tarih :', 'saat :', 'yer :', 'date:', 'time:', 'location:', 'venue:', 'speaker:',
        'تاریخ:', 'ساعت:', 'مکان:', 'مدرس:', 'برگزارکننده:', 'datum:', 'zeit:', 'ort:',
        'дата:', 'время:', 'место:'
    )
    meta_emojis = ('📅', '🕒', '📍', '🗓️', '⏰', '📌', '👨‍🏫', '👩‍🏫', '🎯', '✨', '💚', '🔔', '📢')
    
    lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
    cleaned_sentences = []
    
    title_norm = re.sub(r'[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]', '', title).lower().strip() if title else ''
    
    for l in lines:
        l_lower = l.lower()
        if any(l_lower.startswith(p) for p in meta_prefixes):
            continue
        if any(l.startswith(e) for e in meta_emojis):
            continue
            
        l_norm = re.sub(r'[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]', '', l).lower().strip()
        # Başlıkla aynı veya çok kısa başlıksı satırları atla
        if title_norm and (l_norm == title_norm or (len(l_norm) < 60 and l_norm in title_norm)):
            continue
        if len(l) < 55 and not l.endswith(('.', '!', '?', ';', ':')) and not re.search(r'(dir|tir|dır|tır|cek|cak|miş|mış|yor|du|dü|dı|di)$', l.lower()):
            continue
            
        if not l.endswith(('.', '!', '?', ';')):
            l += '.'
        cleaned_sentences.append(l)
        
    combined = ' '.join(cleaned_sentences)
    combined = re.sub(r'\s+', ' ', combined).strip()
    if not combined:
        return clean_text[:max_chars].strip()
        
    sentences = re.split(r'(?<=[.!?。؛])\s+', combined)
    selected = []
    curr_len = 0
    
    for s in sentences:
        s_clean = s.strip()
        if not s_clean or len(s_clean) < 15:
            continue
        selected.append(s_clean)
        curr_len += len(s_clean)
        if curr_len >= 200 or len(selected) >= 2:
            if curr_len >= 180:
                break
                
    if not selected:
        return combined[:max_chars].strip()
        
    summary = ' '.join(selected)
    if len(summary) > max_chars + 80:
        summary = summary[:max_chars].rsplit(' ', 1)[0]
        if not summary.endswith(('.', '!', '?')):
            summary += '...'
    return summary