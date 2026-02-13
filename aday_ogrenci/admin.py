from django.contrib import admin
from .models import AdayMenu, AdaySayfa, AdaySlider, AdayIletisim

@admin.register(AdayMenu)
class AdayMenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active',]
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']

@admin.register(AdaySayfa)
class AdaySayfaAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'slug', 
        'is_published', 
        'has_downloadable_files',  # ستون جدید
        'created_at'
    ]
    list_editable = ['is_published']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
    # فیلدها در فرم ویرایش
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'content', 'image', 'is_published')
        }),
        ('İndirilebilir Dosyalar', {
            'fields': ('pdf_file', 'word_file', 'excel_file', 'other_file'),
            'classes': ('collapse',)  # قابل جمع شدن
        }),
    )
    
    def has_downloadable_files(self, obj):
        return obj.has_downloadable_files()
    has_downloadable_files.boolean = True
    has_downloadable_files.short_description = 'Dosya Var'

@admin.register(AdaySlider)
class AdaySliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']

@admin.register(AdayIletisim)
class AdayIletisimAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at', 'is_read']
    list_editable = ['is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Seçilen mesajları okundu olarak işaretle"
    
    actions = [mark_as_read]