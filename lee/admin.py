# fen_edebiyat/admin.py
from django.contrib import admin
from .models import LeeDuyuru, Lee_Etkinlik

@admin.register(LeeDuyuru)
class LeeDuyuruAdmin(admin.ModelAdmin):
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
    


@admin.register(Lee_Etkinlik)
class Lee_EtkinlikAdmin(admin.ModelAdmin):
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