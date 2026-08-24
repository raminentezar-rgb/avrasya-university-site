# app_name: elektrik_elektronik_muhendisligi/admin.py

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    ElektrikElektronikMuhendisligiDuyuru, ElektrikElektronikMuhendisligiFaaliyetGrubu, ElektrikElektronikMuhendisligiFaaliyetGorseli, ElektrikElektronikMuhendisligiEtkinlik, ElektrikElektronikMuhendisligiDersProgrami, ElektrikElektronikMuhendisligiFaaliyet
)

@admin.register(ElektrikElektronikMuhendisligiEtkinlik)
class ElektrikElektronikMuhendisligiEtkinlikAdmin(TranslationAdmin):
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

@admin.register(ElektrikElektronikMuhendisligiDuyuru)
class ElektrikElektronikMuhendisligiDuyuruAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'fakulte', 'yayin_tarihi', 'yayinda']
    list_filter = ['yayinda', 'yayin_tarihi']
    search_fields = ['baslik', 'icerik']
    
    def get_queryset(self, request):
        return ElektrikElektronikMuhendisligiDuyuru.objects.all()

@admin.register(ElektrikElektronikMuhendisligiDersProgrami)
class ElektrikElektronikMuhendisligiDersProgramiAdmin(TranslationAdmin):
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

class ElektrikElektronikMuhendisligiFaaliyetGorseliInline(admin.TabularInline):
    model = ElektrikElektronikMuhendisligiFaaliyetGorseli
    extra = 1

@admin.register(ElektrikElektronikMuhendisligiFaaliyetGrubu)
class ElektrikElektronikMuhendisligiFaaliyetGrubuAdmin(TranslationAdmin):
    list_display = ['baslik', 'faaliyet_turu', 'sira']
    list_filter = ['faaliyet_turu']
    list_editable = ['sira']

@admin.register(ElektrikElektronikMuhendisligiFaaliyet)
class ElektrikElektronikMuhendisligiFaaliyetAdmin(TranslationAdmin):
    list_display = ['baslik', 'grup', 'tarih', 'sira']
    list_filter = ['grup__faaliyet_turu', 'grup']
    list_editable = ['sira']
    search_fields = ['baslik', 'icerik']
    inlines = [ElektrikElektronikMuhendisligiFaaliyetGorseliInline]
