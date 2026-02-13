# spor_bilimleri/admin.py
from django.contrib import admin
from .models import SporBilimleriDuyuru

@admin.register(SporBilimleriDuyuru)
class SporBilimleriDuyuruAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'kategori', 'yayin_tarihi', 'yayinda', 'onemli', 'sira']
    list_filter = ['kategori', 'yayinda', 'onemli', 'yayin_tarihi']
    search_fields = ['baslik', 'icerik', 'ozet']
    list_editable = ['yayinda', 'onemli', 'sira']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('baslik', 'icerik', 'ozet', 'kategori', 'ana_duyuru')
        }),
        ('Dosya ve Ayarlar', {
            'fields': ('dosya', 'onemli', 'yayinda', 'sira')
        }),
    )