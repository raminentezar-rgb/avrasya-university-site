from django.contrib import admin
from modeltranslation.admin import TranslationAdmin # اضافه کردن کلاس ترجمه ادمین
from .models import SliderItem, Page
from django.urls import reverse
from django.utils.html import format_html

@admin.register(SliderItem)
class SliderAdmin(TranslationAdmin): # تغییر از admin.ModelAdmin به TranslationAdmin
    list_display = ('title', 'content_type', 'order', 'is_active', 'media_preview')
    list_filter = ('content_type', 'is_active')
    
    # فیلد title_tr, title_en و غیره به صورت خودکار در این بخش ظاهر می‌شوند
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'content_type', 'order', 'is_active', 'link')
        }),
        ('محتوا', {
            'fields': ('image', 'video', 'video_url'),
            'description': 'فقط یکی از فیلدهای تصویر یا ویدیو را پر کنید'
        }),
    )

    def media_preview(self, obj):
        if obj.content_type == 'image' and obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        elif obj.content_type == 'video':
            if obj.video:
                return "ویدیو آپلودی"
            elif obj.video_url:
                return "لینک ویدیو"
        return "بدون رسانه"
    media_preview.short_description = 'پیش‌نمایش'

@admin.register(Page)
class PageAdmin(TranslationAdmin): # تغییر برای پشتیبانی از ترجمه در صفحات
    list_display = ('title', 'slug', 'is_published')
    # فیلدهای title و content به صورت چندزبانه در پنل نمایش داده می‌شوند
    prepopulated_fields = {'slug': ('title',)}

# بخش مربوط به AdayOgrenciAdmin شما بدون تغییر می‌ماند مگر اینکه آن را هم ترجمه کنید