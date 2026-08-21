# app_name: grafik_tasarimi/admin.py

from django.contrib import admin
from .models import (
    GrafikTasarimiFaaliyetGorseli, GrafikTasarimiEtkinlik, GrafikTasarimiDersProgrami, GrafikTasarimiDuyuru, GrafikTasarimiFaaliyetGrubu, GrafikTasarimiFaaliyet
)

@admin.register(GrafikTasarimiEtkinlik)
class GrafikTasarimiEtkinlikAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'etkinlik_turu', 'baslangic_tarihi', 'yer', 'yayinda']
    list_filter = ['etkinlik_turu', 'yayinda', 'baslangic_tarihi', 'kayit_gerekiyor']
    search_fields = ['baslik', 'yer', 'kisa_aciklama']
    prepopulated_fields = {'slug': ['baslik']}
    date_hierarchy = 'baslangic_tarihi'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('baslik', 'slug', 'etkinlik_turu', 'kisa_aciklama', 'detayli_aciklama')
        }),
        ('Tarih ve Yer', {
            'fields': ('baslangic_tarihi', 'bitis_tarihi', 'yer')
        }),
        ('Görsel ve Katılım', {
            'fields': ('afis', 'katilim_linki', 'kayit_gerekiyor', 'ucretli')
        }),
        ('Yayın Ayarları', {
            'fields': ('yayinda',)
        }),
    )

@admin.register(GrafikTasarimiDuyuru)
class GrafikTasarimiDuyuruAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'fakulte', 'yayin_tarihi', 'yayinda']
    list_filter = ['yayinda', 'yayin_tarihi']
    search_fields = ['baslik', 'icerik']
    
    def get_queryset(self, request):
        return GrafikTasarimiDuyuru.objects.all()

@admin.register(GrafikTasarimiDersProgrami)
class GrafikTasarimiDersProgramiAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'sinif', 'yayin_tarihi', 'aktif']
    list_filter = ['sinif', 'aktif', 'yayin_tarihi']
    search_fields = ['baslik', 'aciklama']
    list_editable = ['aktif']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('baslik', 'aciklama', 'dosya')
        }),
        ('Ayarlar', {
            'fields': ('sinif', 'aktif')
        }),
    )

class GrafikTasarimiFaaliyetGorseliInline(admin.TabularInline):
    model = GrafikTasarimiFaaliyetGorseli
    extra = 1

@admin.register(GrafikTasarimiFaaliyetGrubu)
class GrafikTasarimiFaaliyetGrubuAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'faaliyet_turu', 'sira']
    list_filter = ['faaliyet_turu']
    list_editable = ['sira']

@admin.register(GrafikTasarimiFaaliyet)
class GrafikTasarimiFaaliyetAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'grup', 'tarih', 'sira']
    list_filter = ['grup__faaliyet_turu', 'grup']
    list_editable = ['sira']
    search_fields = ['baslik', 'icerik']
    inlines = [GrafikTasarimiFaaliyetGorseliInline]
