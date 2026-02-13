# saglik_hizmetleri_myo/admin.py
from django.contrib import admin
from .models import SaglikHizmetleriMYODuyuru

@admin.register(SaglikHizmetleriMYODuyuru)
class SaglikHizmetleriMYODuyuruAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'kategori', 'yayin_tarihi', 'yayinda', 'onemli', 'sira']
    list_filter = ['kategori', 'yayinda', 'onemli', 'yayin_tarihi']
    search_fields = ['baslik', 'icerik', 'ozet']
    list_editable = ['yayinda', 'onemli', 'sira']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('baslik', 'icerik', 'ozet', 'kategori')
        }),
        ('Dosya ve Ayarlar', {
            'fields': ('dosya', 'onemli', 'yayinda', 'sira')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-onemli', '-yayin_tarihi')