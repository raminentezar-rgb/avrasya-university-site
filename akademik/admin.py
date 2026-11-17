from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline, TranslationStackedInline

from .models import (
    FakulteSayfasi,
    FakulteYonetimUyesi,
    FakulteEkSekme,
    BolumSayfasi,
    BolumYonetimUyesi,
    BolumEkSekme,
    BolumAkademikKadroUyesi,
)


def _apply_ckeditor_widget(db_field, kwargs, rich_prefixes):
    name = db_field.name
    # Attach CKEditor on base, _tr, and _en fields so the edit form remains fast while supporting Turkish & English richly
    is_target = name in rich_prefixes or any(
        name == f"{p}_tr" or name == f"{p}_en" for p in rich_prefixes
    )
    if is_target:
        from ckeditor_uploader.widgets import CKEditorUploadingWidget
        kwargs['widget'] = CKEditorUploadingWidget(config_name='default')
    elif any(name.startswith(f"{p}_") for p in rich_prefixes):
        kwargs['widget'] = forms.Textarea(attrs={'rows': 4, 'style': 'width: 96%;'})


class FakulteYonetimUyesiInline(TranslationTabularInline):
    model = FakulteYonetimUyesi
    extra = 0
    fields = ['ad_soyad', 'gorev', 'eposta', 'telefon', 'fotograf', 'ozgecmis_url', 'sira', 'aktif']
    verbose_name = _('Ek Yönetici')
    verbose_name_plural = _('Ek Yöneticiler (Dekan Yardımcıları vb.)')


class FakulteEkSekmeInline(TranslationStackedInline):
    model = FakulteEkSekme
    extra = 0
    fields = ['baslik', 'alt_baslik', 'ikon', 'icerik', 'sira', 'aktif']
    classes = ['collapse']

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        _apply_ckeditor_widget(db_field, kwargs, ('icerik',))
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)


@admin.register(FakulteSayfasi)
class FakulteSayfasiAdmin(TabbedTranslationAdmin):
    list_display = [
        'fakulte_adi_badge',
        'fakulte_kodu',
        'yonetici_unvan_ad',
        'bolumler_sekmesi_goster',
        'aktif',
        'guncellenme_tarihi',
    ]
    list_filter = ['aktif', 'bolumler_sekmesi_goster']
    search_fields = ['fakulte_adi', 'fakulte_kodu', 'yonetici_unvan_ad', 'tarihce_icerik', 'dekan_mesaji']
    list_editable = ['bolumler_sekmesi_goster', 'aktif']
    inlines = [FakulteYonetimUyesiInline, FakulteEkSekmeInline]

    class Media:
        css = {
            'all': ('akademik/css/akademik_admin.css',)
        }

    fieldsets = (
        (_('Genel Fakülte Bilgileri'), {
            'fields': ('fakulte_kodu', 'fakulte_adi', 'hero_alt_baslik', 'aktif'),
            'description': _('Fakülte veya yüksekokul ana sayfasının üst başlık ve genel ayarları.'),
        }),
        (_('Bölümler Sekmesi ve Yıllık İstatistikler'), {
            'fields': (
                'bolumler_sekmesi_goster',
                'bolumler_baslik',
                'bolumler_alt_baslik',
                'bolumler_giris_icerik',
                ('ogrenci_sayisi', 'akademik_kadro_sayisi'),
                ('uluslararasi_anlasma_sayisi', 'mezun_istihdam_orani'),
            ),
            'classes': ('collapse',),
            'description': _('İsterseniz "Bölümler" sekmesini açıp kapatabilir ve yıllık değişen sayıları güncelleyebilirsiniz.'),
        }),
        (_('1. Tarihçe Sekmesi'), {
            'fields': ('tarihce_baslik', 'tarihce_alt_baslik', 'tarihce_icerik'),
            'description': _('Fakültenin tarihçe sekmesinde görünecek içerik.'),
        }),
        (_('2. Misyon & Vizyon Sekmesi'), {
            'fields': (
                'misyon_vizyon_baslik',
                'misyon_vizyon_alt_baslik',
                'misyon_vizyon_giris',
                'misyon_icerik',
                'vizyon_icerik',
                'temel_degerler_icerik',
            ),
            'description': _('Misyon ve Vizyon kutucukları otomatik olarak site tasarımıyla kart halinde gösterilir.'),
        }),
        (_('3. Dekan / Müdür Mesajı Sekmesi'), {
            'fields': (
                'mesaj_sekme_adi',
                'mesaj_alt_baslik',
                ('yonetici_unvan_ad', 'yonetici_unvan_rozet'),
                'yonetici_gorevi',
                ('yonetici_eposta', 'yonetici_telefon', 'ziyaret_saatleri'),
                'yonetici_fotografi',
                'dekan_mesaji',
            ),
            'description': _('Dekan veya Yüksekokul Müdürü profili ve mesajı.'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        rich_fields = (
            'bolumler_giris_icerik',
            'tarihce_icerik',
            'misyon_vizyon_giris',
            'misyon_icerik',
            'vizyon_icerik',
            'temel_degerler_icerik',
            'dekan_mesaji',
        )
        _apply_ckeditor_widget(db_field, kwargs, rich_fields)
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)

    def fakulte_adi_badge(self, obj):
        return format_html(
            '<span class="avrasya-admin-badge navy">{}</span>',
            obj.get_localized('fakulte_adi', obj.get_fakulte_kodu_display()),
        )
    fakulte_adi_badge.short_description = _('Fakülte / Birim')


class BolumAkademikKadroInline(admin.StackedInline):
    model = BolumAkademikKadroUyesi
    extra = 1
    fields = (
        ('ad_soyad', 'unvan_gorev_tr', 'kadro_turu'),
        ('eposta', 'telefon', 'oda'),
        ('uzmanlik_alani_tr', 'ozgecmis_url'),
        ('fotograf', 'sira', 'aktif'),
        'biyografi_tr',
    )
    verbose_name = _('Akademik Kadro Üyesi')
    verbose_name_plural = _('6. Sekme İçeriği: Bölüm Öğretim Üyeleri / Akademik Kadro')

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        if db_field.name == 'biyografi_tr':
            kwargs['widget'] = forms.Textarea(attrs={'rows': 2, 'style': 'width: 96%;', 'placeholder': _('Kısa akademik not veya özgeçmiş özeti (Opsiyonel)')})
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)


class BolumYonetimUyesiInline(TranslationTabularInline):
    model = BolumYonetimUyesi
    extra = 0
    fields = ['ad_soyad', 'gorev', 'eposta', 'telefon', 'fotograf', 'ozgecmis_url', 'sira', 'aktif']
    classes = ['collapse']
    verbose_name = _('Ek Yönetici')
    verbose_name_plural = _('Ek Bölüm Yöneticileri (Başkan Yrd. / Koordinatör)')


class BolumEkSekmeInline(TranslationStackedInline):
    model = BolumEkSekme
    extra = 0
    fields = ['baslik', 'alt_baslik', 'ikon', 'icerik', 'sira', 'aktif']
    classes = ['collapse']

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        _apply_ckeditor_widget(db_field, kwargs, ('icerik',))
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)


@admin.register(BolumSayfasi)
class BolumSayfasiAdmin(TabbedTranslationAdmin):
    list_display = [
        'bolum_adi_badge',
        'fakulte_bilgi',
        'baskan_unvan_ad',
        'kadro_sayisi',
        'program_turu',
        'aktif',
        'guncellenme_tarihi',
    ]
    list_filter = ['aktif', 'bolum__fakulte', 'program_turu']
    search_fields = ['bolum_adi', 'bolum_kodu', 'fakulte_adi', 'baskan_unvan_ad', 'tarihce_icerik']
    list_editable = ['aktif']
    autocomplete_fields = ['bolum']
    inlines = [BolumAkademikKadroInline, BolumYonetimUyesiInline, BolumEkSekmeInline]

    class Media:
        css = {
            'all': ('akademik/css/akademik_admin.css',)
        }

    fieldsets = (
        (_('Genel Bölüm / Program Bilgileri'), {
            'fields': ('bolum', 'bolum_kodu', 'bolum_adi', 'fakulte_adi', 'program_turu', 'aktif'),
            'description': _('Her bölüm veya ön lisans programının temel bilgileri.'),
        }),
        (_('1. Sekme: Tarihçe'), {
            'fields': ('tarihce_baslik', 'tarihce_alt_baslik', 'tarihce_icerik'),
        }),
        (_('2. Sekme: Misyon & Vizyon'), {
            'fields': (
                'misyon_vizyon_baslik',
                'misyon_vizyon_alt_baslik',
                'misyon_icerik',
                'vizyon_icerik',
                'amaclari_icerik',
            ),
            'description': _('Misyon ve Vizyon içerikleri ayrı şık kartlarda otomatik biçimlendirilir.'),
        }),
        (_('3. Sekme: Ne İş Yaparlar?'), {
            'fields': ('ne_is_yaparlar_baslik', 'ne_is_yaparlar_alt_baslik', 'ne_is_yaparlar_icerik'),
        }),
        (_('4. Sekme: Mezunlar Nerede Çalışırlar?'), {
            'fields': ('mezunlar_calisma_baslik', 'mezunlar_calisma_alt_baslik', 'mezunlar_calisma_icerik'),
        }),
        (_('5. Sekme: Yönetim (Bölüm / Program Başkanı)'), {
            'fields': (
                'yonetim_baslik',
                'yonetim_alt_baslik',
                ('baskan_unvan_ad', 'baskan_gorev_etiketi'),
                'baskan_unvan_detay',
                ('baskan_eposta', 'baskan_telefon'),
                ('baskan_oda', 'baskan_ofis_saatleri'),
                ('baskan_fotograf', 'baskan_ozgecmis_url'),
                'baskan_mesaji',
            ),
            'description': _('Yönetim sekmesindeki bölüm başkanı profil kartı ve mesajı.'),
        }),
        (_('6. Sekme: Akademik Kadro Ayarları'), {
            'fields': ('kadro_baslik', 'kadro_alt_baslik', 'kadro_aciklama'),
            'description': _('Akademik Kadro sekmesinin başlığı ve üst açıklaması. Öğretim üyelerini hemen aşağıdaki "Bölüm Öğretim Üyeleri" panelinden ekleyebilirsiniz.'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        rich_fields = (
            'tarihce_icerik',
            'misyon_icerik',
            'vizyon_icerik',
            'amaclari_icerik',
            'ne_is_yaparlar_icerik',
            'mezunlar_calisma_icerik',
            'baskan_mesaji',
            'kadro_aciklama',
        )
        _apply_ckeditor_widget(db_field, kwargs, rich_fields)
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)

    def kadro_sayisi(self, obj):
        cnt = obj.akademik_kadro.filter(aktif=True).count()
        return format_html('<span class="avrasya-admin-badge cyan">{} Kişi</span>', cnt)
    kadro_sayisi.short_description = _('Akademik Kadro')

    def bolum_adi_badge(self, obj):
        return format_html(
            '<span class="avrasya-admin-badge blue">{}</span>',
            obj.get_localized('bolum_adi', obj.bolum_kodu),
        )
    bolum_adi_badge.short_description = _('Bölüm / Program')

    def fakulte_bilgi(self, obj):
        if obj.bolum:
            return obj.bolum.get_fakulte_display()
        return obj.fakulte_adi or '-'
    fakulte_bilgi.short_description = _('Fakülte / MYO')


@admin.register(BolumAkademikKadroUyesi)
class BolumAkademikKadroUyesiAdmin(TabbedTranslationAdmin):
    list_display = ['ad_soyad', 'bolum_sayfasi', 'unvan_gorev', 'kadro_turu', 'eposta', 'sira', 'aktif']
    list_filter = ['kadro_turu', 'aktif', 'bolum_sayfasi__bolum__fakulte', 'bolum_sayfasi']
    search_fields = ['ad_soyad', 'unvan_gorev', 'eposta', 'uzmanlik_alani', 'bolum_sayfasi__bolum_adi']
    list_editable = ['sira', 'aktif']
    autocomplete_fields = ['bolum_sayfasi']

    class Media:
        css = {
            'all': ('akademik/css/akademik_admin.css',)
        }

    fieldsets = (
        (_('Bölüm ve Öğretim Elemanı Bilgileri'), {
            'fields': ('bolum_sayfasi', 'ad_soyad', 'unvan_gorev', 'kadro_turu', 'uzmanlik_alani'),
        }),
        (_('İletişim ve Profil'), {
            'fields': ('eposta', 'telefon', 'oda', 'ozgecmis_url', 'fotograf', 'biyografi'),
        }),
        (_('Sıralama ve Yayın Durumu'), {
            'fields': ('sira', 'aktif'),
        }),
    )
