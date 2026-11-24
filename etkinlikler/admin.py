import csv
from io import BytesIO

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.db.models import Count, Max, Q
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from .models import (
    Etkinlik,
    EtkinlikBildirimAboneligi,
    EtkinlikDosya,
    EtkinlikGorsel,
    EtkinlikKayit,
    EtkinlikKonusmaci,
    validate_etkinlik_file,
    validate_etkinlik_image,
)


def _safe_spreadsheet_cell(value) -> str:
    """Neutralize formula injection characters when exporting CSV/Excel."""
    s = "" if value is None else str(value)
    if s and s[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + s
    return s


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Django 5/6 compatible multi-file form field."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(item, initial) for item in data if item]
        if not data:
            return []
        return [single_file_clean(data, initial)]


class EtkinlikAdminForm(forms.ModelForm):
    bulk_images = MultipleFileField(
        required=False,
        label='Toplu Görsel Yükle (Çoklu Seçim)',
        help_text=(
            'Birden fazla görseli (JPG, PNG, WEBP, GIF) Ctrl/Shift ile seçip tek seferde '
            'galeriye ekleyebilirsiniz. Adet sınırı yoktur.'
        ),
        widget=MultipleFileInput(
            attrs={'multiple': True, 'accept': '.jpg,.jpeg,.png,.webp,.gif'}
        ),
    )
    bulk_files = MultipleFileField(
        required=False,
        label='Toplu PDF / Excel / Dosya Yükle (Çoklu Seçim)',
        help_text=(
            'Birden fazla PDF, Excel (.xls, .xlsx, .xlsm, .csv), Word veya görsel dosyasını '
            'tek seferde ekleyebilirsiniz. Dosya türü ve adı otomatik tanımlanır; adet sınırı yoktur.'
        ),
        widget=MultipleFileInput(
            attrs={
                'multiple': True,
                'accept': '.pdf,.xls,.xlsx,.xlsm,.csv,.doc,.docx,.jpg,.jpeg,.png,.webp,.gif',
            }
        ),
    )

    class Meta:
        model = Etkinlik
        fields = '__all__'

    def clean_bulk_images(self):
        files = self.cleaned_data.get('bulk_images') or []
        for f in files:
            validate_etkinlik_image(f)
        return files

    def clean_bulk_files(self):
        files = self.cleaned_data.get('bulk_files') or []
        for f in files:
            validate_etkinlik_file(f)
        return files


class EtkinlikKonusmaciInline(admin.TabularInline):
    model = EtkinlikKonusmaci
    extra = 1
    fields = ('foto_onizleme', 'ad_soyad', 'unvan', 'kurum', 'fotograf', 'bio', 'sira')
    readonly_fields = ('foto_onizleme',)

    def foto_onizleme(self, obj):
        if obj and obj.fotograf:
            return format_html(
                '<img src="{}" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover;" />',
                obj.fotograf.url,
            )
        return '-'

    foto_onizleme.short_description = 'Fotoğraf'


class EtkinlikGorselInline(admin.TabularInline):
    model = EtkinlikGorsel
    extra = 1
    fields = ('onizleme', 'gorsel', 'baslik', 'sira')
    readonly_fields = ('onizleme',)

    def onizleme(self, obj):
        if obj and obj.gorsel:
            return format_html(
                '<a href="{0}" target="_blank" rel="noopener">'
                '<img src="{0}" style="max-height: 55px; max-width: 85px; border-radius: 6px; object-fit: cover;" />'
                '</a>',
                obj.gorsel.url,
            )
        return '-'

    onizleme.short_description = 'Önizleme'


class EtkinlikDosyaInline(admin.TabularInline):
    model = EtkinlikDosya
    extra = 1
    fields = ('dosya_onizleme', 'dosya', 'dosya_adi', 'dosya_turu', 'aciklama', 'sira')
    readonly_fields = ('dosya_onizleme',)

    def dosya_onizleme(self, obj):
        if not obj or not obj.dosya:
            return '-'
        if obj.is_image:
            return format_html(
                '<a href="{0}" target="_blank" rel="noopener">'
                '<img src="{0}" style="max-height: 45px; max-width: 70px; border-radius: 4px; object-fit: cover;" />'
                '</a>',
                obj.dosya.url,
            )
        return format_html(
            '<a href="{0}" target="_blank" rel="noopener" style="font-weight: 600;">{1} ({2})</a>',
            obj.dosya.url,
            obj.get_dosya_turu_display() or obj.file_extension or 'Dosya',
            obj.get_file_size(),
        )

    dosya_onizleme.short_description = 'Mevcut Dosya'


@admin.register(Etkinlik)
class EtkinlikAdmin(TranslationAdmin):
    form = EtkinlikAdminForm
    list_display = [
        'baslik',
        'etkinlik_turu',
        'fakulte',
        'baslangic_tarihi',
        'yer',
        'yayinda',
        'kayit_sayisi',
        'gorsel_sayisi',
        'dosya_sayisi',
    ]
    list_filter = ['etkinlik_turu', 'fakulte', 'yayinda', 'baslangic_tarihi', 'kayit_gerekiyor', 'ucretli']
    search_fields = ['baslik', 'yer', 'duzenleyen', 'kisa_aciklama']
    prepopulated_fields = {'slug': ['baslik']}
    date_hierarchy = 'baslangic_tarihi'
    inlines = [EtkinlikKonusmaciInline, EtkinlikGorselInline, EtkinlikDosyaInline]

    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('baslik', 'slug', 'etkinlik_turu', 'fakulte', 'duzenleyen', 'kisa_aciklama', 'detayli_aciklama')
        }),
        ('Tarih, Yer ve Harita', {
            'fields': ('baslangic_tarihi', 'bitis_tarihi', 'yer', 'harita_linki')
        }),
        ('Görsel ve Katılım / Kontenjan', {
            'fields': ('afis', 'katilim_linki', 'kayit_gerekiyor', 'kontenjan', 'son_kayit_tarihi', 'ucretli')
        }),
        ('Toplu Dosya ve Görsel Yükleme (Sınırsız Adet)', {
            'fields': ('bulk_images', 'bulk_files'),
            'description': (
                'Aşağıdaki satırları tek tek doldurmaya ek olarak, buradan aynı anda birden fazla '
                'görsel, PDF veya Excel dosyasını seçip kaydedebilirsiniz.'
            ),
        }),
        ('Yayın Ayarları', {
            'fields': ('yayinda',)
        }),
    )

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        if db_field.name == 'detayli_aciklama' or db_field.name.startswith('detayli_aciklama_'):
            kwargs['widget'] = CKEditorUploadingWidget(config_name='default')
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _gorsel_count=Count('gorseller', distinct=True),
            _dosya_count=Count('dosyalar', distinct=True),
            _kayit_count=Count('kayitlar', filter=~Q(kayitlar__durum='iptal'), distinct=True),
        )

    def kayit_sayisi(self, obj):
        cnt = getattr(obj, '_kayit_count', obj.kayitlar.exclude(durum='iptal').count())
        if obj.kontenjan:
            return f"{cnt} / {obj.kontenjan}"
        return cnt

    kayit_sayisi.short_description = 'Kayıt'

    def gorsel_sayisi(self, obj):
        return getattr(obj, '_gorsel_count', obj.gorseller.count())

    gorsel_sayisi.short_description = 'Görsel'

    def dosya_sayisi(self, obj):
        return getattr(obj, '_dosya_count', obj.dosyalar.count())

    dosya_sayisi.short_description = 'Dosya'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance

        bulk_images = form.cleaned_data.get('bulk_images') or []
        if bulk_images:
            next_img_order = (obj.gorseller.aggregate(m=Max('sira'))['m'] or 0) + 1
            for offset, img_file in enumerate(bulk_images):
                EtkinlikGorsel.objects.create(
                    etkinlik=obj,
                    gorsel=img_file,
                    sira=next_img_order + offset,
                )

        bulk_files = form.cleaned_data.get('bulk_files') or []
        if bulk_files:
            next_file_order = (obj.dosyalar.aggregate(m=Max('sira'))['m'] or 0) + 1
            for offset, attached in enumerate(bulk_files):
                EtkinlikDosya.objects.create(
                    etkinlik=obj,
                    dosya=attached,
                    sira=next_file_order + offset,
                )

    class Media:
        js = (
            'etkinlikler/js/auto_summary.js',
        )
        css = {
            'all': ('etkinlikler/css/auto_summary.css',)
        }


@admin.register(EtkinlikGorsel)
class EtkinlikGorselAdmin(admin.ModelAdmin):
    list_display = ('etkinlik', 'image_preview', 'baslik', 'sira', 'olusturulma_tarihi')
    list_filter = ('etkinlik',)
    search_fields = ('baslik', 'etkinlik__baslik')
    list_select_related = ('etkinlik',)

    def image_preview(self, obj):
        if obj.gorsel:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 75px; border-radius: 4px; object-fit: cover;" />',
                obj.gorsel.url,
            )
        return '-'

    image_preview.short_description = 'Önizleme'


@admin.register(EtkinlikDosya)
class EtkinlikDosyaAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'etkinlik', 'dosya_turu', 'file_size_col', 'file_link', 'olusturulma_tarihi')
    list_filter = ('dosya_turu', 'etkinlik')
    search_fields = ('dosya_adi', 'aciklama', 'etkinlik__baslik')
    list_select_related = ('etkinlik',)

    def file_size_col(self, obj):
        return obj.get_file_size()

    file_size_col.short_description = 'Boyut'

    def file_link(self, obj):
        if obj.dosya:
            return format_html('<a href="{}" target="_blank" rel="noopener">İndir / Görüntüle</a>', obj.dosya.url)
        return '-'

    file_link.short_description = 'Dosya'


@admin.register(EtkinlikKayit)
class EtkinlikKayitAdmin(admin.ModelAdmin):
    list_display = ('kayit_kodu', 'ad_soyad', 'email', 'telefon', 'etkinlik', 'durum', 'olusturulma_tarihi')
    list_filter = ('durum', 'etkinlik', 'olusturulma_tarihi')
    search_fields = ('kayit_kodu', 'ad_soyad', 'email', 'telefon', 'ogrenci_no', 'etkinlik__baslik')
    readonly_fields = ('kayit_kodu', 'olusturulma_tarihi')
    list_select_related = ('etkinlik',)
    actions = ['export_xlsx', 'export_csv']

    @admin.action(description='Seçili kayıtları Excel (.xlsx) olarak indir')
    def export_xlsx(self, request, queryset):
        try:
            import openpyxl
        except ImportError:
            return self.export_csv(request, queryset)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Etkinlik Kayıtları"
        headers = [
            "Kayıt Kodu", "Etkinlik", "Ad Soyad", "E-posta", "Telefon",
            "Öğrenci / TC No", "Fakülte / Kurum", "Not", "Durum", "Kayıt Tarihi",
        ]
        ws.append(headers)

        for row in queryset.select_related('etkinlik'):
            ws.append([
                _safe_spreadsheet_cell(row.kayit_kodu),
                _safe_spreadsheet_cell(row.etkinlik.baslik),
                _safe_spreadsheet_cell(row.ad_soyad),
                _safe_spreadsheet_cell(row.email),
                _safe_spreadsheet_cell(row.telefon),
                _safe_spreadsheet_cell(row.ogrenci_no),
                _safe_spreadsheet_cell(row.kurum_fakulte),
                _safe_spreadsheet_cell(row.notlar),
                _safe_spreadsheet_cell(row.get_durum_display()),
                timezone.localtime(row.olusturulma_tarihi).strftime('%d.%m.%Y %H:%M'),
            ])

        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)
        response = HttpResponse(
            buf.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="etkinlik_kayitlari.xlsx"'
        return response

    @admin.action(description='Seçili kayıtları CSV (.csv) olarak indir')
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
        response["Content-Disposition"] = 'attachment; filename="etkinlik_kayitlari.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Kayıt Kodu", "Etkinlik", "Ad Soyad", "E-posta", "Telefon",
            "Öğrenci / TC No", "Fakülte / Kurum", "Not", "Durum", "Kayıt Tarihi",
        ])
        for row in queryset.select_related('etkinlik'):
            writer.writerow([
                _safe_spreadsheet_cell(row.kayit_kodu),
                _safe_spreadsheet_cell(row.etkinlik.baslik),
                _safe_spreadsheet_cell(row.ad_soyad),
                _safe_spreadsheet_cell(row.email),
                _safe_spreadsheet_cell(row.telefon),
                _safe_spreadsheet_cell(row.ogrenci_no),
                _safe_spreadsheet_cell(row.kurum_fakulte),
                _safe_spreadsheet_cell(row.notlar),
                _safe_spreadsheet_cell(row.get_durum_display()),
                timezone.localtime(row.olusturulma_tarihi).strftime('%d.%m.%Y %H:%M'),
            ])
        return response


@admin.register(EtkinlikBildirimAboneligi)
class EtkinlikBildirimAboneligiAdmin(admin.ModelAdmin):
    list_display = ('email', 'ad_soyad', 'tercih_turu', 'aktif', 'olusturulma_tarihi')
    list_filter = ('aktif', 'tercih_turu', 'olusturulma_tarihi')
    search_fields = ('email', 'ad_soyad')
    readonly_fields = ('iptal_token', 'olusturulma_tarihi')
