from django.contrib import admin
from .models import (
    News, Announcement, Category
)
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'news_type', 'category', 'is_featured', 
        'is_published', 'published_at', 'views_count', 'image_preview'
    ]
    list_filter = ['news_type', 'is_featured', 'is_published', 'category', 'published_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'image_preview']
    list_editable = ['is_featured', 'is_published']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        (_('Başlık ve Tür'), {
            'fields': ('title', 'slug', 'news_type', 'category', 'author')
        }),
        (_('Görsel'), {
            'fields': ('image', 'image_alt', 'image_preview')
        }),
        (_('İçerik'), {
            'fields': ('summary', 'content')
        }),
        (_('Yayın Ayarları'), {
            'fields': ('is_featured', 'is_published', 'published_at')
        }),
        (_('İstatistikler'), {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return _('Görsel Yok')
    image_preview.short_description = _('Önizleme')
    
    actions = ['make_published', 'make_featured', 'make_unfeatured']
    
    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = _('Seçilenleri Yayınla')
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = _('Seçilenleri Öne Çıkar')
    
    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
    make_unfeatured.short_description = _('Öne Çıkarılanı Kaldır')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'announcement_date', 'is_important', 'is_active', 'created_at']
    list_filter = ['is_important', 'is_active', 'announcement_date']
    search_fields = ['title', 'content', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_important', 'is_active']
    date_hierarchy = 'announcement_date'
    
    fieldsets = (
        (_('Başlık'), {
            'fields': ('title', 'slug')
        }),
        (_('İçerik'), {
            'fields': ('summary', 'content', 'image')
        }),
        (_('Dış Link'), {
            'fields': ('external_link', 'external_link_text'),
            'classes': ('collapse',)
        }),
        (_('Ayarlar'), {
            'fields': ('announcement_date', 'is_important', 'is_active')
        }),
        (_('Zaman Damgaları'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )