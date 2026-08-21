from django.contrib import admin
from .models import (
    InternationalApplication
)

@admin.register(InternationalApplication)
class InternationalApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'program', 'created_at')
    list_filter = ('program', 'semester', 'education_level', 'country')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'birth_date', 'gender', 'email', 'phone')
        }),
        ('Address Information', {
            'fields': ('country', 'city', 'address')
        }),
        ('Academic Information', {
            'fields': ('program', 'semester', 'education_level', 'english_level')
        }),
        ('Documents', {
            'fields': ('passport_copy', 'diploma_certificate', 'academic_transcript', 'passport_photo')
        }),
        ('Meta', {
            'fields': ('newsletter_subscription', 'created_at')
        }),
    )
