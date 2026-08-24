# app_name: fizyoterapi_rehabilitasyon/admin.py

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    FizyoterapiRehabilitasyonDersProgrami, FizyoterapiRehabilitasyonFaaliyetGorseli, FizyoterapiRehabilitasyonEtkinlik, FizyoterapiRehabilitasyonDuyuru, FizyoterapiRehabilitasyonFaaliyetGrubu, FizyoterapiRehabilitasyonFaaliyet
)

@admin.register(FizyoterapiRehabilitasyonEtkinlik)
class FizyoterapiRehabilitasyonEtkinlikAdmin(TranslationAdmin):
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

@admin.register(FizyoterapiRehabilitasyonDuyuru)
class FizyoterapiRehabilitasyonDuyuruAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'fakulte', 'yayin_tarihi', 'yayinda']
    list_filter = ['yayinda', 'yayin_tarihi']
    search_fields = ['baslik', 'icerik']
    
    def get_queryset(self, request):
        return FizyoterapiRehabilitasyonDuyuru.objects.all()

@admin.register(FizyoterapiRehabilitasyonDersProgrami)
class FizyoterapiRehabilitasyonDersProgramiAdmin(TranslationAdmin):
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

class FizyoterapiRehabilitasyonFaaliyetGorseliInline(admin.TabularInline):
    model = FizyoterapiRehabilitasyonFaaliyetGorseli
    extra = 1

@admin.register(FizyoterapiRehabilitasyonFaaliyetGrubu)
class FizyoterapiRehabilitasyonFaaliyetGrubuAdmin(TranslationAdmin):
    list_display = ['baslik', 'faaliyet_turu', 'sira']
    list_filter = ['faaliyet_turu']
    list_editable = ['sira']

@admin.register(FizyoterapiRehabilitasyonFaaliyet)
class FizyoterapiRehabilitasyonFaaliyetAdmin(TranslationAdmin):
    list_display = ['baslik', 'grup', 'tarih', 'sira']
    list_filter = ['grup__faaliyet_turu', 'grup']
    list_editable = ['sira']
    search_fields = ['baslik', 'icerik']
    inlines = [FizyoterapiRehabilitasyonFaaliyetGorseliInline]
