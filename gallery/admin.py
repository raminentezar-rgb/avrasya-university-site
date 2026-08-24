from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    GalleryImage, GalleryCategory
)

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']

@admin.register(GalleryImage)
class GalleryImageAdmin(TranslationAdmin):
    list_display = ['title', 'category', 'upload_date', 'is_active', 'order']
    list_filter = ['category', 'is_active', 'upload_date']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    date_hierarchy = 'upload_date'