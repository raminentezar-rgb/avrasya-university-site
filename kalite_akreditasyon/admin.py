from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    Category, News, Announcement, Mevzuat,
    Takim, Rapor, Izleme, Dokuman, SSS
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_published', 'published_at', 'views_count']
    list_filter = ['is_featured', 'is_published', 'category', 'published_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at']
    list_editable = ['is_featured', 'is_published']


@admin.register(Announcement)
class AnnouncementAdmin(TranslationAdmin):
    list_display = ['title', 'announcement_date', 'is_important', 'is_active', 'has_document']
    list_filter = ['is_important', 'is_active', 'announcement_date']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at']
    list_editable = ['is_important', 'is_active']

    def has_document(self, obj):
        return bool(obj.document)
    has_document.boolean = True
    has_document.short_description = _('Belge')


@admin.register(Mevzuat)
class MevzuatAdmin(TranslationAdmin):
    list_display = ['title', 'mevzuat_type', 'order', 'is_active']
    list_filter = ['mevzuat_type', 'is_active']
    search_fields = ['title']
    list_editable = ['order', 'is_active']


@admin.register(Takim)
class TakimAdmin(TranslationAdmin):
    list_display = ['name', 'title', 'role', 'department', 'email', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'role', 'department', 'email']
    list_editable = ['order', 'is_active']


@admin.register(Rapor)
class RaporAdmin(TranslationAdmin):
    list_display = ['title', 'rapor_type', 'year', 'order', 'is_active']
    list_filter = ['rapor_type', 'year', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']


@admin.register(Izleme)
class IzlemeAdmin(TranslationAdmin):
    list_display = ['title', 'izleme_type', 'year', 'order', 'is_active']
    list_filter = ['izleme_type', 'year', 'is_active']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_active']


@admin.register(Dokuman)
class DokumanAdmin(TranslationAdmin):
    list_display = ['title', 'doc_code', 'dokuman_type', 'revision_no', 'order', 'is_active']
    list_filter = ['dokuman_type', 'is_active']
    search_fields = ['title', 'doc_code', 'description']
    list_editable = ['order', 'is_active']


@admin.register(SSS)
class SSSAdmin(TranslationAdmin):
    list_display = ['question', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
