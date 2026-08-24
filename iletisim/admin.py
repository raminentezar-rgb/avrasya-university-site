# iletisim/admin.py
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    IletisimDuyuru
)

@admin.register(IletisimDuyuru)
class IletisimDuyuruAdmin(TranslationAdmin):
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