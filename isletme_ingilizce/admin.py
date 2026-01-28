from django.contrib import admin
from .models import IsletmeIngilizceDuyuru, IsletmeIngilizce_Etkinlik, DersProgramiDosyaIsletmeIngilizce

@admin.register(IsletmeIngilizce_Etkinlik)
class IsletmeIngilizce_EtkinlikAdmin(admin.ModelAdmin):
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

@admin.register(IsletmeIngilizceDuyuru)
class IsletmeIngilizceDuyuruAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'fakulte', 'yayin_tarihi', 'yayinda']
    list_filter = ['yayinda', 'yayin_tarihi']
    search_fields = ['baslik', 'icerik']
    
    def get_queryset(self, request):
        return IsletmeIngilizceDuyuru.objects.all()

@admin.register(DersProgramiDosyaIsletmeIngilizce)
class DersProgramiDosyaIsletmeIngilizceAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'sinif', 'akademik_yil', 'dosya_turu', 'yayin_tarihi', 'sira', 'aktif']
    list_filter = [
        'sinif', 
        'akademik_yil', 
        'dosya_turu', 
        'aktif', 
        'yayin_tarihi'
    ]
    search_fields = ['baslik', 'aciklama']
    list_editable = ['sira', 'aktif']
    date_hierarchy = 'yayin_tarihi'
    ordering = ['sinif', 'sira']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('baslik', 'aciklama', 'dosya')
        }),
        ('Sınıflandırma', {
            'fields': ('sinif', 'akademik_yil', 'dosya_turu')
        }),
        ('Ayarlar', {
            'fields': ('sira', 'aktif', 'yayin_tarihi')
        }),
    )