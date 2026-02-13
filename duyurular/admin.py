from django.contrib import admin
from .models import Duyuru, DuyuruDosya, Bolum
from modeltranslation.admin import TranslationAdmin

class BolumAdmin(admin.ModelAdmin):
    list_display = ['ad', 'kod', 'fakulte', 'aktif']
    list_filter = ['fakulte', 'aktif']
    search_fields = ['ad', 'kod']
    prepopulated_fields = {'kod': ['ad']}

class DuyuruDosyaInline(admin.TabularInline):
    model = DuyuruDosya
    extra = 1
    fields = ['dosya', 'dosya_adi', 'tur', 'aciklama']
    verbose_name = "Dosya"
    verbose_name_plural = "Dosyalar"

@admin.register(Duyuru)
class DuyuruAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'fakulte', 'get_bolumler', 'yayin_tarihi', 'yayinda', 'olusturulma_tarihi', 'dosya_sayisi']
    list_filter = ['fakulte', 'yayinda', 'yayin_tarihi', 'bolumler']
    search_fields = ['baslik', 'icerik']
    prepopulated_fields = {'slug': ['baslik']}
    date_hierarchy = 'yayin_tarihi'
    filter_horizontal = ['bolumler']
    inlines = [DuyuruDosyaInline]
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('baslik', 'slug', 'fakulte', 'ozet', 'icerik')
        }),
        ('Bölüm Seçimi', {
            'fields': ('bolumler',),
            'description': 'Bu duyurunun gösterileceği bölümleri seçin. En az bir bölüm seçilmelidir.'
        }),
        ('Tarih ve Yayın', {
            'fields': ('yayin_tarihi', 'yayinda')
        }),
    )
    
    def get_bolumler(self, obj):
        return obj.get_bolum_adlari()
    get_bolumler.short_description = 'İlgili Bölümler'
    
    def dosya_sayisi(self, obj):
        return obj.dosyalar.count()
    dosya_sayisi.short_description = 'Dosya Sayısı'

@admin.register(DuyuruDosya)
class DuyuruDosyaAdmin(admin.ModelAdmin):
    list_display = ['dosya_adi', 'duyuru', 'fakulte', 'tur', 'olusturulma_tarihi']
    list_filter = ['tur', 'olusturulma_tarihi', 'duyuru__fakulte']
    search_fields = ['dosya_adi', 'duyuru__baslik']
    list_select_related = ['duyuru']
    
    def fakulte(self, obj):
        return obj.duyuru.get_fakulte_display()
    fakulte.short_description = 'Fakülte'

admin.site.register(Bolum, BolumAdmin)