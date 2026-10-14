from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    """Kategori Modeli"""
    name = models.CharField(_('Kategori Adı'), max_length=150)
    slug = models.SlugField(_('Slug'), max_length=150, unique=True)
    is_active = models.BooleanField(_('Aktif'), default=True)
    order = models.PositiveIntegerField(_('Sıralama'), default=0)

    class Meta:
        verbose_name = _('Kategori')
        verbose_name_plural = _('Kategoriler')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class News(models.Model):
    """Haberler Modeli"""
    title = models.CharField(_('Başlık'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Kategori'),
        related_name='news'
    )
    summary = models.TextField(
        _('Özet'),
        max_length=500,
        blank=True,
        help_text=_('Haber listesinde görünecek kısa özet')
    )
    content = models.TextField(_('İçerik'))
    image = models.ImageField(
        _('Haber Görseli'),
        upload_to='kalite_akreditasyon/news/%Y/%m/',
        blank=True,
        null=True
    )
    is_featured = models.BooleanField(_('Öne Çıkan'), default=False)
    is_published = models.BooleanField(_('Yayında'), default=True)
    published_at = models.DateTimeField(_('Yayın Tarihi'), default=timezone.now)
    views_count = models.PositiveIntegerField(_('Görüntülenme'), default=0)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)

    class Meta:
        verbose_name = _('Haber')
        verbose_name_plural = _('Haberler')
        ordering = ['-is_featured', '-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('kalite_akreditasyon:haber_detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/core/img/default-news.jpg'


class Announcement(models.Model):
    """Duyurular Modeli"""
    title = models.CharField(_('Başlık'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True, blank=True)
    summary = models.TextField(
        _('Özet'),
        max_length=400,
        blank=True
    )
    content = models.TextField(_('İçerik'))
    document = models.FileField(
        _('Ek Dosya (PDF/Word/Excel)'),
        upload_to='kalite_akreditasyon/announcements/%Y/',
        blank=True,
        null=True
    )
    external_link = models.URLField(_('Harici Bağlantı Linki'), blank=True, null=True)
    announcement_date = models.DateField(_('Duyuru Tarihi'), default=timezone.now)
    is_important = models.BooleanField(_('Önemli Duyuru'), default=False)
    is_active = models.BooleanField(_('Aktif'), default=True)
    views_count = models.PositiveIntegerField(_('Görüntülenme'), default=0)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)

    class Meta:
        verbose_name = _('Duyuru')
        verbose_name_plural = _('Duyurular')
        ordering = ['-is_important', '-announcement_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('kalite_akreditasyon:duyuru_detail', kwargs={'slug': self.slug})

    def get_day(self):
        return self.announcement_date.day

    def get_month_short(self):
        months = {
            1: 'Oca', 2: 'Şub', 3: 'Mar', 4: 'Nis',
            5: 'May', 6: 'Haz', 7: 'Tem', 8: 'Ağu',
            9: 'Eyl', 10: 'Eki', 11: 'Kas', 12: 'Ara'
        }
        return months.get(self.announcement_date.month, '')

    def get_year(self):
        return self.announcement_date.year


class Mevzuat(models.Model):
    """Mevzuat Modeli"""
    MEVZUAT_TYPES = [
        ('kanun', _('Kanun ve KHK')),
        ('yonetmelik', _('Yönetmelik')),
        ('yonerge', _('Yönerge')),
        ('esas', _('Usul ve Esaslar')),
        ('senato', _('Senato Kararları')),
        ('diger', _('Diğer')),
    ]

    title = models.CharField(_('Mevzuat Başlığı'), max_length=255)
    mevzuat_type = models.CharField(_('Türü'), max_length=30, choices=MEVZUAT_TYPES, default='yonerge')
    file = models.FileField(_('Dosya (PDF)'), upload_to='kalite_akreditasyon/mevzuat/%Y/', blank=True, null=True)
    external_link = models.URLField(_('Mevzuat Linki'), blank=True, null=True)
    order = models.PositiveIntegerField(_('Sıralama'), default=0)
    is_active = models.BooleanField(_('Aktif'), default=True)
    created_at = models.DateTimeField(_('Tarih'), auto_now_add=True)

    class Meta:
        verbose_name = _('Mevzuat')
        verbose_name_plural = _('Mevzuat')
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Takim(models.Model):
    """Takım / Ekip Modeli"""
    name = models.CharField(_('Adı Soyadı'), max_length=150)
    title = models.CharField(_('Akademik / İdari Unvanı'), max_length=100, blank=True)
    role = models.CharField(_('Görevi / Pozisyonu'), max_length=120)
    department = models.CharField(_('Birimi / Bölümü'), max_length=150, blank=True)
    email = models.EmailField(_('E-posta'), blank=True)
    phone = models.CharField(_('Telefon / Dahili'), max_length=50, blank=True)
    photo = models.ImageField(
        _('Fotoğraf'),
        upload_to='kalite_akreditasyon/takim/',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(_('Sıralama'), default=0)
    is_active = models.BooleanField(_('Aktif'), default=True)

    class Meta:
        verbose_name = _('Takım Üyesi')
        verbose_name_plural = _('Takım')
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.title} {self.name} - {self.role}"


class Rapor(models.Model):
    """Raporlar Modeli"""
    RAPOR_TYPES = [
        ('kidr', _('Kurum İç Değerlendirme Raporu (KİDR)')),
        ('kdr', _('Kurum Dış Değerlendirme Raporu')),
        ('izleme', _('İzleme Raporu')),
        ('faaliyet', _('Faaliyet Raporu')),
        ('anket', _('Anket Değerlendirme Raporu')),
        ('diger', _('Diğer Raporlar')),
    ]

    title = models.CharField(_('Rapor Adı'), max_length=255)
    rapor_type = models.CharField(_('Rapor Türü'), max_length=30, choices=RAPOR_TYPES, default='kidr')
    year = models.PositiveIntegerField(_('Yıl / Dönem'), default=2026)
    file = models.FileField(_('Rapor Dosyası (PDF)'), upload_to='kalite_akreditasyon/raporlar/%Y/')
    description = models.TextField(_('Açıklama / Özet'), blank=True)
    order = models.PositiveIntegerField(_('Sıralama'), default=0)
    is_active = models.BooleanField(_('Aktif'), default=True)
    created_at = models.DateTimeField(_('Tarih'), auto_now_add=True)

    class Meta:
        verbose_name = _('Rapor')
        verbose_name_plural = _('Raporlar')
        ordering = ['order', '-year', 'title']

    def __str__(self):
        return f"{self.title} ({self.year})"


class Izleme(models.Model):
    """İzleme Modeli"""
    IZLEME_TYPES = [
        ('gosterge', _('Performans Göstergeleri')),
        ('puko', _('PUKÖ Çevrimleri & İyileştirmeler')),
        ('surec', _('Süreç İzleme ve Riskler')),
        ('anket', _('Paydaş Memnuniyet İzleme')),
        ('diger', _('Diğer İzleme Faaliyetleri')),
    ]

    title = models.CharField(_('İzleme Faaliyeti Başlığı'), max_length=255)
    izleme_type = models.CharField(_('Türü'), max_length=30, choices=IZLEME_TYPES, default='puko')
    content = models.TextField(_('Açıklama / Detay'), blank=True)
    file = models.FileField(_('İlgili Belge / Dosya'), upload_to='kalite_akreditasyon/izleme/%Y/', blank=True, null=True)
    year = models.PositiveIntegerField(_('Dönem / Yıl'), default=2026)
    order = models.PositiveIntegerField(_('Sıralama'), default=0)
    is_active = models.BooleanField(_('Aktif'), default=True)

    class Meta:
        verbose_name = _('İzleme Faaliyeti')
        verbose_name_plural = _('İzleme')
        ordering = ['order', '-year', 'title']

    def __str__(self):
        return self.title


class Dokuman(models.Model):
    """Doküman Modeli"""
    DOKUMAN_TYPES = [
        ('el_kitabi', _('Kalite El Kitabı')),
        ('form', _('Formlar & Şablonlar')),
        ('surec', _('Süreç Kartları & İş Akışları')),
        ('rehber', _('Kılavuz ve Rehberler')),
        ('politika', _('Politika Belgeleri')),
        ('diger', _('Diğer Dokümanlar')),
    ]

    title = models.CharField(_('Doküman Adı'), max_length=255)
    doc_code = models.CharField(_('Doküman Kodu'), max_length=50, blank=True, help_text=_('Örn: FR-01, KL-02'))
    dokuman_type = models.CharField(_('Türü'), max_length=30, choices=DOKUMAN_TYPES, default='form')
    file = models.FileField(_('Dosya (PDF/Word/Excel)'), upload_to='kalite_akreditasyon/dokumanlar/%Y/')
    description = models.TextField(_('Açıklama'), blank=True)
    revision_no = models.CharField(_('Revizyon No / Tarih'), max_length=50, blank=True, default='00')
    order = models.PositiveIntegerField(_('Sıralama'), default=0)
    is_active = models.BooleanField(_('Aktif'), default=True)

    class Meta:
        verbose_name = _('Doküman')
        verbose_name_plural = _('Doküman')
        ordering = ['dokuman_type', 'order', 'title']

    def __str__(self):
        return self.title


class SSS(models.Model):
    """S.S.S (Sıkça Sorulan Sorular) Modeli"""
    question = models.CharField(_('Soru'), max_length=300)
    answer = models.TextField(_('Cevap'))
    order = models.PositiveIntegerField(_('Sıralama'), default=0)
    is_active = models.BooleanField(_('Aktif'), default=True)

    class Meta:
        verbose_name = _('S.S.S')
        verbose_name_plural = _('S.S.S')
        ordering = ['order', 'question']

    def __str__(self):
        return self.question
