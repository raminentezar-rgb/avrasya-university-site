from django.contrib import admin
from .models import (
    NewsImage, News, NewsAttachment
)
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ('image', 'caption', 'order')
    classes = ('collapse',)

class NewsAttachmentInline(admin.TabularInline):
    model = NewsAttachment
    extra = 1
    fields = ('file', 'title', 'file_type', 'description')
    classes = ('collapse',)

@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'published_at', 'is_published', 'image_count', 'attachment_count')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published',)
    search_fields = ('title', 'summary', 'content')
    inlines = [NewsImageInline, NewsAttachmentInline]
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'تعداد تصاویر'
    
    def attachment_count(self, obj):
        return obj.attachments.count()
    attachment_count.short_description = 'تعداد پیوست‌ها'

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('news', 'image_preview', 'caption', 'order')
    list_filter = ('news',)
    search_fields = ('caption', 'news__title')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'پیش‌نمایش'

@admin.register(NewsAttachment)
class NewsAttachmentAdmin(admin.ModelAdmin):
    list_display = ('news', 'title', 'file_type', 'file_preview', 'created_at')
    list_filter = ('file_type', 'news')
    search_fields = ('title', 'description', 'news__title')
    
    def file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">📄 دانلود</a>', obj.file.url)
        return "-"
    file_preview.short_description = 'فایل'