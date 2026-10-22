from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    Category, News, Announcement, Mevzuat,
    Takim, Rapor, Izleme, Dokuman, SSS,
    BolumKalite, BolumKaliteDosya
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_published', 'published_at', 'views_count']
    list_filter = ['is_featured', 'is_published', 'category', 'published_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at']
    list_editable = ['is_featured', 'is_published']


@admin.register(Announcement)
class AnnouncementAdmin(TranslationAdmin):
    list_display = ['title', 'announcement_date', 'is_important', 'is_active', 'has_document']
    list_filter = ['is_important', 'is_active', 'announcement_date']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at']
    list_editable = ['is_important', 'is_active']

    def has_document(self, obj):
        return bool(obj.document)
    has_document.boolean = True
    has_document.short_description = _('Belge')


@admin.register(Mevzuat)
class MevzuatAdmin(TranslationAdmin):
    list_display = ['title', 'mevzuat_type', 'order', 'is_active']
    list_filter = ['mevzuat_type', 'is_active']
    search_fields = ['title']
    list_editable = ['order', 'is_active']


@admin.register(Takim)
class TakimAdmin(TranslationAdmin):
    list_display = ['name', 'title', 'role', 'department', 'email', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'role', 'department', 'email']
    list_editable = ['order', 'is_active']


@admin.register(Rapor)
class RaporAdmin(TranslationAdmin):
    list_display = ['title', 'rapor_type', 'year', 'order', 'is_active']
    list_filter = ['rapor_type', 'year', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']


@admin.register(Izleme)
class IzlemeAdmin(TranslationAdmin):
    list_display = ['title', 'izleme_type', 'year', 'order', 'is_active']
    list_filter = ['izleme_type', 'year', 'is_active']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_active']


@admin.register(Dokuman)
class DokumanAdmin(TranslationAdmin):
    list_display = ['title', 'doc_code', 'dokuman_type', 'revision_no', 'order', 'is_active']
    list_filter = ['dokuman_type', 'is_active']
    search_fields = ['title', 'doc_code', 'description']
    list_editable = ['order', 'is_active']


@admin.register(SSS)
class SSSAdmin(TranslationAdmin):
    list_display = ['question', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']


from django import forms

class BolumKaliteDosyaInlineForm(forms.ModelForm):
    class Meta:
        model = BolumKaliteDosya
        fields = '__all__'
        widgets = {
            'dosya_adi': forms.TextInput(attrs={
                'placeholder': _('Dosya adı (Opsiyonel)'),
                'style': 'width: 100%; min-width: 160px;'
            }),
            'aciklama': forms.TextInput(attrs={
                'placeholder': _('Kısa açıklama (Opsiyonel)'),
                'style': 'width: 100%; min-width: 190px;'
            }),
            'sira': forms.NumberInput(attrs={
                'style': 'width: 60px; text-align: center;'
            }),
        }


class BolumKaliteDosyaInline(admin.TabularInline):
    model = BolumKaliteDosya
    form = BolumKaliteDosyaInlineForm
    extra = 2
    fields = ['dosya', 'dosya_adi', 'tur', 'aciklama', 'sira']
    verbose_name = _("Ekli Dosya")
    verbose_name_plural = _("Ekli Dosyalar (İndirilebilir Belgeler)")


@admin.register(BolumKalite)
class BolumKaliteAdmin(TranslationAdmin):
    list_display = ['bolum', 'get_sekme_display_badge', 'baslik', 'aktif', 'dosya_sayisi', 'guncellenme_tarihi']
    list_filter = ['sekme', 'aktif', 'bolum__fakulte', 'bolum']
    search_fields = ['bolum__ad', 'bolum__kod', 'baslik', 'icerik']
    list_editable = ['aktif']
    inlines = [BolumKaliteDosyaInline]

    class Media:
        css = {
            'all': ('kalite_akreditasyon/css/kalite_admin.css',)
        }

    fieldsets = (
        (_('Bölüm ve Sekme Bilgisi'), {
            'fields': ('bolum', 'sekme', 'baslik', 'aktif')
        }),
        (_('İçerik'), {
            'fields': ('icerik',),
            'description': _('Zengin metin editörünü kullanarak tablo, görsel ve biçimlendirilmiş metin ekleyebilirsiniz.')
        }),
    )

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        if db_field.name == 'icerik' or db_field.name.startswith('icerik_'):
            from ckeditor_uploader.widgets import CKEditorUploadingWidget
            kwargs['widget'] = CKEditorUploadingWidget(config_name='default')
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)

    def dosya_sayisi(self, obj):
        return obj.dosyalar.count()
    dosya_sayisi.short_description = _('Dosya Sayısı')

    def get_sekme_display_badge(self, obj):
        colors = {
            'tab1': '#0d6efd',
            'tab2': '#6610f2',
            'tab3': '#0dcaf0',
            'tab4': '#198754',
            'tab5': '#ffc107',
            'tab6': '#fd7e14',
        }
        color = colors.get(obj.sekme, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px;">{}</span>',
            color,
            obj.get_sekme_display()
        )
    get_sekme_display_badge.short_description = _('Sekme')


@admin.register(BolumKaliteDosya)
class BolumKaliteDosyaAdmin(TranslationAdmin):
    list_display = ['dosya_adi', 'kalite', 'tur', 'sira', 'olusturulma_tarihi']
    list_filter = ['tur', 'kalite__sekme', 'kalite__bolum']
    search_fields = ['dosya_adi', 'aciklama', 'kalite__bolum__ad']
