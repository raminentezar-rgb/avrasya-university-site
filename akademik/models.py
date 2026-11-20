from django.db import models
from django.utils.translation import gettext_lazy as _


class LocalizedContentMixin:
    """Aktif dilde içerik boşsa Türkçe (_tr) veya ana alana güvenli geri dönüş sağlar."""

    def get_localized(self, field_name, default=""):
        val = getattr(self, field_name, None)
        if val and str(val).strip():
            return val
        tr_val = getattr(self, f"{field_name}_tr", None)
        if tr_val and str(tr_val).strip():
            return tr_val
        base_val = self.__dict__.get(field_name)
        if base_val and str(base_val).strip():
            return base_val
        return default


class FakulteSayfasi(LocalizedContentMixin, models.Model):
    """Fakülte / Yüksekokul / MYO Ana Sayfa Dinamik Sekme İçerikleri"""

    FAKULTE_CHOICES = [
        ('fen_edebiyat', _('İnsan ve Toplum Bilimleri Fakültesi')),
        ('iktisadi_idari', _('İktisadi ve İdari Bilimler Fakültesi')),
        ('muhendislik_mimarlik', _('Mühendislik ve Mimarlık Fakültesi')),
        ('saglik_bilimleri', _('Sağlık Bilimleri Fakültesi')),
        ('spor_bilimleri', _('Spor Bilimleri Fakültesi')),
        ('iletisim', _('İletişim Fakültesi')),
        ('uygulamali_bilimler', _('Uygulamalı Bilimler Yüksekokulu')),
        ('meslek_yuksekokulu', _('Meslek Yüksekokulu')),
        ('saglik_hizmetleri_myo', _('Sağlık Hizmetleri Meslek Yüksekokulu')),
        ('lee', _('Lisansüstü Eğitim Enstitüsü')),
    ]

    fakulte_kodu = models.CharField(
        _('Fakülte / Birim Kodu'),
        max_length=60,
        unique=True,
        choices=FAKULTE_CHOICES,
    )
    fakulte_adi = models.CharField(
        _('Fakülte / Birim Adı'),
        max_length=255,
    )
    hero_alt_baslik = models.CharField(
        _('Üst Banner Alt Başlığı (Opsiyonel)'),
        max_length=300,
        blank=True,
    )

    # Bölümler Sekmesi Ayarları
    bolumler_sekmesi_goster = models.BooleanField(
        _('Bölümler Sekmesini Göster'),
        default=True,
        help_text=_('İşaretli ise "Bölümler" sekmesi ilk sekme olarak görüntülenir. Kaldırılırsa sadece Tarihçe, Misyon & Vizyon ve Dekan/Müdür Mesajı gösterilir.'),
    )
    bolumler_baslik = models.CharField(
        _('Bölümler Sekme Adı'),
        max_length=150,
        default='Bölümler',
    )
    bolumler_alt_baslik = models.CharField(
        _('Bölümler Sekme Alt Başlığı'),
        max_length=300,
        blank=True,
    )
    bolumler_giris_icerik = models.TextField(
        _('Bölümler Tanıtım Metni (Opsiyonel)'),
        blank=True,
    )
    bolumler_liste_baslik = models.CharField(
        _('Bölümler Liste Başlığı'),
        max_length=200,
        default='Lisans Programları',
        blank=True,
    )
    bolumler_liste_aciklama = models.CharField(
        _('Bölümler Liste Açıklaması'),
        max_length=400,
        default='Aşağıda fakültemiz bünyesindeki programlar hakkında detaylı bilgileri bulabilirsiniz:',
        blank=True,
    )

    # Yıllık Değişebilen Fakülte İstatistikleri
    istatistikleri_goster = models.BooleanField(_('İstatistik Kartlarını Göster'), default=True)
    istatistik_1_baslik = models.CharField(_('1. İstatistik Etiketi'), max_length=100, default='Toplam Öğrenci', blank=True)
    ogrenci_sayisi = models.CharField(_('1. İstatistik Değeri'), max_length=50, blank=True)
    istatistik_2_baslik = models.CharField(_('2. İstatistik Etiketi'), max_length=100, default='Akademik Kadro', blank=True)
    akademik_kadro_sayisi = models.CharField(_('2. İstatistik Değeri'), max_length=50, blank=True)
    istatistik_3_baslik = models.CharField(_('3. İstatistik Etiketi'), max_length=100, default='Uluslararası Anlaşma', blank=True)
    uluslararasi_anlasma_sayisi = models.CharField(_('3. İstatistik Değeri'), max_length=50, blank=True)
    istatistik_4_baslik = models.CharField(_('4. İstatistik Etiketi'), max_length=100, default='Mezun İstihdam Oranı', blank=True)
    mezun_istihdam_orani = models.CharField(_('4. İstatistik Değeri (%)'), max_length=50, blank=True)

    # Sekme: Tarihçe
    tarihce_baslik = models.CharField(
        _('Tarihçe Sekme Adı'),
        max_length=150,
        default='Tarihçe',
    )
    tarihce_alt_baslik = models.CharField(
        _('Tarihçe Alt Başlığı'),
        max_length=300,
        blank=True,
    )
    tarihce_icerik = models.TextField(
        _('Tarihçe İçeriği'),
        blank=True,
        help_text=_('Zengin metin editörü ile Tarihçe metnini düzenleyebilirsiniz.'),
    )

    # Sekme: Misyon & Vizyon
    misyon_vizyon_baslik = models.CharField(
        _('Misyon & Vizyon Sekme Adı'),
        max_length=150,
        default='Misyon & Vizyon',
    )
    misyon_vizyon_alt_baslik = models.CharField(
        _('Misyon & Vizyon Alt Başlığı'),
        max_length=300,
        blank=True,
    )
    misyon_vizyon_giris = models.TextField(
        _('Misyon & Vizyon Giriş Metni (Opsiyonel)'),
        blank=True,
    )
    misyon_icerik = models.TextField(
        _('Misyonumuz'),
        blank=True,
    )
    vizyon_icerik = models.TextField(
        _('Vizyonumuz'),
        blank=True,
    )
    temel_degerler_icerik = models.TextField(
        _('Temel Değerler / Alıntı (Opsiyonel)'),
        blank=True,
    )

    # Sekme: Dekan / Müdür Mesajı
    mesaj_sekme_adi = models.CharField(
        _('Mesaj Sekme Adı'),
        max_length=150,
        default='Dekan Mesajı',
        help_text=_('Örn: Dekan Mesajı veya Müdür Mesajı'),
    )
    mesaj_alt_baslik = models.CharField(
        _('Mesaj Sekmesi Alt Başlığı'),
        max_length=300,
        blank=True,
    )
    yonetici_unvan_ad = models.CharField(
        _('Dekan / Müdür Adı ve Unvanı'),
        max_length=200,
        blank=True,
        help_text=_('Örn: Prof. Dr. Mustafa EMİR'),
    )
    yonetici_gorevi = models.CharField(
        _('Yönetici Görevi'),
        max_length=255,
        blank=True,
        help_text=_('Örn: İnsan ve Toplum Bilimleri Fakültesi Dekanı'),
    )
    yonetici_unvan_rozet = models.CharField(
        _('Akademik Unvan Rozeti (Opsiyonel)'),
        max_length=120,
        blank=True,
    )
    yonetici_eposta = models.CharField(_('E-posta'), max_length=150, blank=True)
    yonetici_telefon = models.CharField(_('Telefon'), max_length=60, blank=True)
    ziyaret_saatleri = models.CharField(_('Ziyaret Saatleri'), max_length=120, blank=True)
    yonetici_fotografi = models.ImageField(
        _('Yönetici Fotoğrafı'),
        upload_to='akademik/fakulte_yonetim/',
        blank=True,
        null=True,
    )
    dekan_mesaji = models.TextField(
        _('Dekan / Müdür Mesajı'),
        blank=True,
    )

    aktif = models.BooleanField(_('Yayında'), default=True)
    guncellenme_tarihi = models.DateTimeField(_('Son Güncelleme'), auto_now=True)

    class Meta:
        verbose_name = _('Fakülte Sayfası')
        verbose_name_plural = _('Fakülte Ana Sayfa İçerikleri')
        ordering = ['fakulte_adi']

    def __str__(self):
        return self.get_localized('fakulte_adi', self.get_fakulte_kodu_display())


class FakulteYonetimUyesi(LocalizedContentMixin, models.Model):
    """Fakülte Mesaj / Yönetim Sekmesinde Gösterilebilecek Ek Yönetici (Dekan Yardımcısı vb.)"""

    fakulte = models.ForeignKey(
        FakulteSayfasi,
        on_delete=models.CASCADE,
        related_name='ek_yoneticiler',
        verbose_name=_('Fakülte Sayfası'),
    )
    ad_soyad = models.CharField(_('Ad Soyad ve Unvan'), max_length=200)
    gorev = models.CharField(_('Görevi'), max_length=200, help_text=_('Örn: Dekan Yardımcısı'))
    eposta = models.CharField(_('E-posta'), max_length=150, blank=True)
    telefon = models.CharField(_('Telefon'), max_length=60, blank=True)
    fotograf = models.ImageField(_('Fotoğraf'), upload_to='akademik/fakulte_yonetim/', blank=True, null=True)
    ozgecmis_url = models.CharField(_('Özgeçmiş / Profil Linki'), max_length=500, blank=True)
    sira = models.PositiveIntegerField(_('Sıra'), default=0)
    aktif = models.BooleanField(_('Aktif'), default=True)

    class Meta:
        verbose_name = _('Ek Yönetici')
        verbose_name_plural = _('Ek Yöneticiler (Dekan Yardımcıları vb.)')
        ordering = ['sira', 'id']

    def __str__(self):
        return f"{self.ad_soyad} - {self.gorev}"


class FakulteEkSekme(LocalizedContentMixin, models.Model):
    """Fakülte Ana Sayfası İçin İsteğe Bağlı Ek Özel Sekme"""

    fakulte = models.ForeignKey(
        FakulteSayfasi,
        on_delete=models.CASCADE,
        related_name='ek_sekmeler',
        verbose_name=_('Fakülte Sayfası'),
    )
    baslik = models.CharField(_('Sekme Başlığı'), max_length=150)
    alt_baslik = models.CharField(_('Alt Başlık (Opsiyonel)'), max_length=300, blank=True)
    ikon = models.CharField(_('FontAwesome İkon Sınıfı'), max_length=80, default='fas fa-layer-group')
    icerik = models.TextField(_('Sekme İçeriği'), blank=True)
    sira = models.PositiveIntegerField(_('Sıralama'), default=1)
    aktif = models.BooleanField(_('Yayında'), default=True)

    class Meta:
        verbose_name = _('Ek Özel Sekme')
        verbose_name_plural = _('Ek Özel Sekmeler')
        ordering = ['sira', 'id']

    def __str__(self):
        return f"{self.fakulte.fakulte_adi} - {self.baslik}"


class FakulteBolumKarti(LocalizedContentMixin, models.Model):
    """Fakülte Bölümler Sekmesindeki Bölüm / Program Kartları"""

    fakulte = models.ForeignKey(
        FakulteSayfasi,
        on_delete=models.CASCADE,
        related_name='bolum_kartlari',
        verbose_name=_('Fakülte Sayfası'),
    )
    ad = models.CharField(_('Bölüm / Program Adı'), max_length=200)
    kisa_kod = models.CharField(
        _('Kısa Kod (Rozet)'),
        max_length=24,
        blank=True,
        help_text=_('Örn: İDE, PSK, ADL'),
    )
    ikon = models.CharField(
        _('FontAwesome İkon'),
        max_length=80,
        default='fas fa-graduation-cap',
        blank=True,
    )
    program_turu = models.CharField(
        _('Derece / Program Türü'),
        max_length=120,
        default='Lisans Derecesi',
        blank=True,
    )
    egitim_dili = models.CharField(_('Eğitim Dili'), max_length=120, default='Türkçe', blank=True)
    egitim_suresi = models.CharField(_('Eğitim Süresi'), max_length=80, default='4 Yıl', blank=True)
    aciklama = models.TextField(_('Kısa Açıklama'), blank=True)
    detay_url = models.CharField(
        _('Detaylı Bilgi Linki'),
        max_length=300,
        blank=True,
        help_text=_('Örn: /ingiliz_dili_edebiyati/'),
    )
    sira = models.PositiveIntegerField(_('Sıralama'), default=0)
    aktif = models.BooleanField(_('Yayında'), default=True)

    class Meta:
        verbose_name = _('Fakülte Bölüm Kartı')
        verbose_name_plural = _('Fakülte Bölümler Kartları')
        ordering = ['sira', 'id']

    def __str__(self):
        return f"{self.ad} ({self.fakulte.fakulte_adi})"


class BolumSayfasi(LocalizedContentMixin, models.Model):
    """Bölüm / Program Ana Sayfa Dinamik 5 Sekmeli İçerik Modeli"""

    bolum = models.OneToOneField(
        'duyurular.Bolum',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sayfa_icerigi',
        verbose_name=_('Bağlı Bölüm Kaydı'),
    )
    bolum_kodu = models.SlugField(
        _('Bölüm / Uygulama Kodu'),
        max_length=120,
        unique=True,
        help_text=_('URL ve Django uygulama koduyla eşleşir (Örn: ingiliz_dili_edebiyati).'),
    )
    bolum_adi = models.CharField(
        _('Bölüm / Program Adı'),
        max_length=255,
    )
    fakulte_adi = models.CharField(
        _('Bağlı Olduğu Fakülte / MYO'),
        max_length=255,
        blank=True,
    )
    program_turu = models.CharField(
        _('Program Düzeyi'),
        max_length=100,
        default='Lisans Programı',
        blank=True,
    )

    # 1. Sekme: Tarihçe
    tarihce_baslik = models.CharField(_('1. Sekme Adı'), max_length=150, default='Tarihçe')
    tarihce_alt_baslik = models.CharField(_('Tarihçe Üst Başlığı'), max_length=255, blank=True)
    tarihce_icerik = models.TextField(_('Tarihçe İçeriği'), blank=True)

    # 2. Sekme: Misyon & Vizyon
    misyon_vizyon_baslik = models.CharField(_('2. Sekme Adı'), max_length=150, default='Misyon & Vizyon')
    misyon_vizyon_alt_baslik = models.CharField(_('Misyon & Vizyon Üst Başlığı'), max_length=255, blank=True)
    misyon_icerik = models.TextField(_('Misyonumuz'), blank=True)
    vizyon_icerik = models.TextField(_('Vizyonumuz'), blank=True)
    amaclari_icerik = models.TextField(_('Eğitim Amaçları / Temel Değerler (Opsiyonel)'), blank=True)

    # 3. Sekme: Ne İş Yaparlar?
    ne_is_yaparlar_baslik = models.CharField(_('3. Sekme Adı'), max_length=150, default='Ne İş Yaparlar?')
    ne_is_yaparlar_alt_baslik = models.CharField(_('Ne İş Yaparlar Üst Başlığı'), max_length=255, blank=True)
    ne_is_yaparlar_icerik = models.TextField(_('Ne İş Yaparlar İçeriği'), blank=True)

    # 4. Sekme: Mezunlar Nerede Çalışırlar?
    mezunlar_calisma_baslik = models.CharField(_('4. Sekme Adı'), max_length=150, default='Mezunlar Nerede Çalışırlar?')
    mezunlar_calisma_alt_baslik = models.CharField(_('Mezunlar Nerede Çalışırlar Üst Başlığı'), max_length=255, blank=True)
    mezunlar_calisma_icerik = models.TextField(_('Mezunlar Nerede Çalışırlar İçeriği'), blank=True)

    # 5. Sekme: Yönetim
    yonetim_baslik = models.CharField(_('5. Sekme Adı'), max_length=150, default='Yönetim')
    yonetim_alt_baslik = models.CharField(_('Yönetim Üst Başlığı'), max_length=255, default='Bölüm Yönetimi')
    baskan_unvan_ad = models.CharField(
        _('Bölüm Başkanı Adı ve Unvanı'),
        max_length=200,
        blank=True,
        help_text=_('Örn: Dr. Öğr. Üyesi Rukiye ÖZTÜRK'),
    )
    baskan_gorev_etiketi = models.CharField(
        _('Durum Rozeti'),
        max_length=120,
        default='Bölüm Başkanı',
        blank=True,
        help_text=_('Örn: Bölüm Başkanı veya Bölüm Başkan Vekili'),
    )
    baskan_unvan_detay = models.CharField(
        _('Görev Tanımı'),
        max_length=255,
        blank=True,
        help_text=_('Örn: İngiliz Dili ve Edebiyatı Bölümü Bölüm Başkan V.'),
    )
    baskan_eposta = models.CharField(_('E-posta'), max_length=150, blank=True)
    baskan_telefon = models.CharField(_('Telefon'), max_length=60, blank=True)
    baskan_oda = models.CharField(_('Oda / Yerleşke'), max_length=150, blank=True)
    baskan_ofis_saatleri = models.CharField(_('Ofis Saatleri'), max_length=150, blank=True)
    baskan_fotograf = models.ImageField(
        _('Bölüm Başkanı Fotoğrafı'),
        upload_to='akademik/bolum_yonetim/',
        blank=True,
        null=True,
    )
    baskan_ozgecmis_url = models.CharField(_('Özgeçmiş / AVESİS Bağlantısı'), max_length=500, blank=True)
    baskan_mesaji = models.TextField(_('Bölüm Başkanı Mesajı / Ek Bilgiler (Opsiyonel)'), blank=True)

    # 6. Sekme: Akademik Kadro
    kadro_baslik = models.CharField(_('6. Sekme Adı'), max_length=150, default='Akademik Kadro')
    kadro_alt_baslik = models.CharField(_('Akademik Kadro Üst Başlığı'), max_length=255, default='Akademik Kadro')
    kadro_aciklama = models.TextField(_('Akademik Kadro Açıklaması (Opsiyonel)'), blank=True)

    aktif = models.BooleanField(_('Yayında'), default=True)
    guncellenme_tarihi = models.DateTimeField(_('Son Güncelleme'), auto_now=True)

    class Meta:
        verbose_name = _('Bölüm / Program Sayfası')
        verbose_name_plural = _('Bölüm ve Program Ana Sayfa İçerikleri')
        ordering = ['fakulte_adi', 'bolum_adi']

    def __str__(self):
        return f"{self.get_localized('bolum_adi', self.bolum_kodu)}"


class BolumYonetimUyesi(LocalizedContentMixin, models.Model):
    """Bölüm Yönetim Sekmesi İçin Ek Yönetici Üyeleri (Bölüm Başkan Yrd., Koordinatör vb.)"""

    bolum_sayfasi = models.ForeignKey(
        BolumSayfasi,
        on_delete=models.CASCADE,
        related_name='ek_yoneticiler',
        verbose_name=_('Bölüm Sayfası'),
    )
    ad_soyad = models.CharField(_('Ad Soyad ve Unvan'), max_length=200)
    gorev = models.CharField(_('Görevi'), max_length=200, help_text=_('Örn: Bölüm Başkan Yardımcısı'))
    eposta = models.CharField(_('E-posta'), max_length=150, blank=True)
    telefon = models.CharField(_('Telefon'), max_length=60, blank=True)
    fotograf = models.ImageField(_('Fotoğraf'), upload_to='akademik/bolum_yonetim/', blank=True, null=True)
    ozgecmis_url = models.CharField(_('Özgeçmiş Linki'), max_length=500, blank=True)
    sira = models.PositiveIntegerField(_('Sıra'), default=0)
    aktif = models.BooleanField(_('Aktif'), default=True)

    class Meta:
        verbose_name = _('Ek Yönetici')
        verbose_name_plural = _('Ek Yöneticiler (Başkan Yrd. / Koordinatörler)')
        ordering = ['sira', 'id']

    def __str__(self):
        return f"{self.ad_soyad} - {self.gorev}"


class BolumEkSekme(LocalizedContentMixin, models.Model):
    """Bölüm Ana Sayfası İçin İsteğe Bağlı Ek Özel Sekme"""

    bolum_sayfasi = models.ForeignKey(
        BolumSayfasi,
        on_delete=models.CASCADE,
        related_name='ek_sekmeler',
        verbose_name=_('Bölüm Sayfası'),
    )
    baslik = models.CharField(_('Sekme Başlığı'), max_length=150)
    alt_baslik = models.CharField(_('Alt Başlık (Opsiyonel)'), max_length=300, blank=True)
    ikon = models.CharField(_('FontAwesome İkon Sınıfı'), max_length=80, default='fas fa-layer-group')
    icerik = models.TextField(_('Sekme İçeriği'), blank=True)
    sira = models.PositiveIntegerField(_('Sıralama'), default=1)
    aktif = models.BooleanField(_('Yayında'), default=True)

    class Meta:
        verbose_name = _('Ek Özel Sekme')
        verbose_name_plural = _('Ek Özel Sekmeler')
        ordering = ['sira', 'id']

    def __str__(self):
        return f"{self.bolum_sayfasi.bolum_adi} - {self.baslik}"


class BolumAkademikKadroUyesi(LocalizedContentMixin, models.Model):
    """Bölüm Akademik Kadro Sekmesi İçin Öğretim Üyesi / Elemanı Bilgileri"""

    KADRO_TURU_CHOICES = [
        ('akademik', _('Akademik Kadro')),
        ('misafir', _('Misafir Öğretim Elemanı')),
    ]

    bolum_sayfasi = models.ForeignKey(
        BolumSayfasi,
        on_delete=models.CASCADE,
        related_name='akademik_kadro',
        verbose_name=_('Bölüm / Program'),
    )
    ad_soyad = models.CharField(
        _('Ad Soyad ve Unvan'),
        max_length=220,
        help_text=_('Örn: Prof. Dr. Mustafa EMİR'),
    )
    unvan_gorev = models.CharField(
        _('Unvan / Görev'),
        max_length=180,
        blank=True,
        default='Öğretim Üyesi',
        help_text=_('Örn: Bölüm Başkanı, Dr. Öğr. Üyesi, Arş. Gör., Öğr. Gör.'),
    )
    kadro_turu = models.CharField(
        _('Kadro Türü'),
        max_length=30,
        choices=KADRO_TURU_CHOICES,
        default='akademik',
    )
    uzmanlik_alani = models.CharField(
        _('Çalışma / Uzmanlık Alanı'),
        max_length=300,
        blank=True,
    )
    eposta = models.CharField(_('E-posta'), max_length=150, blank=True)
    telefon = models.CharField(_('Telefon'), max_length=60, blank=True, default='+90 462 334 05 50')
    oda = models.CharField(_('Oda / Ofis'), max_length=120, blank=True)
    ozgecmis_url = models.CharField(_('Özgeçmiş / AVESİS Bağlantısı'), max_length=500, blank=True)
    fotograf = models.ImageField(
        _('Fotoğraf (Opsiyonel)'),
        upload_to='akademik/bolum_kadro/',
        blank=True,
        null=True,
    )
    biyografi = models.TextField(_('Kısa Özgeçmiş / Not (Opsiyonel)'), blank=True)
    sira = models.PositiveIntegerField(_('Sıra'), default=0)
    aktif = models.BooleanField(_('Yayında'), default=True)

    class Meta:
        verbose_name = _('Akademik Kadro Üyesi')
        verbose_name_plural = _('Akademik Kadro (Öğretim Elemanları)')
        ordering = ['sira', 'id']

    def __str__(self):
        return f"{self.ad_soyad} ({self.bolum_sayfasi.bolum_adi})"
