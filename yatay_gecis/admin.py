from django.contrib import admin
from django.utils.html import format_html
from .models import CallbackRequest

@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'email', 'created_at', 'is_processed', 'action_buttons']
    list_filter = ['is_processed', 'created_at', 'accept_communication', 'accept_kvkk']
    search_fields = ['full_name', 'email', 'phone', 'notes']
    readonly_fields = ['created_at', 'ip_address', 'user_agent']
    list_editable = ['is_processed']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Kişi Bilgileri', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Onaylar', {
            'fields': ('accept_communication', 'accept_kvkk'),
            'classes': ('wide',)
        }),
        ('Durum', {
            'fields': ('is_processed', 'notes')
        }),
        ('Sistem Bilgileri', {
            'fields': ('created_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def action_buttons(self, obj):
        return format_html(
            '<a class="button" href="mailto:{}" target="_blank">📧 E-posta</a> '
            '<a class="button" href="tel:{}" style="background: #28a745;">📞 Ara</a>',
            obj.email, obj.phone
        )
    action_buttons.short_description = 'İşlemler'
    action_buttons.allow_tags = True
    
    actions = ['mark_as_processed', 'send_reminder_email']
    
    def mark_as_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        self.message_user(request, f'{updated} talep işlendi olarak işaretlendi.')
    mark_as_processed.short_description = 'Seçili talepleri işlendi olarak işaretle'
    
    def send_reminder_email(self, request, queryset):
        from django.core.mail import send_mail
        for obj in queryset.filter(is_processed=False):
            send_mail(
                'Geri Arama Talebi Hatırlatması',
                f'Sayın Yetkili,\n\n{obj.full_name} tarafından {obj.created_at.strftime("%d.%m.%Y")} tarihinde yapılan geri arama talebi henüz işleme alınmamıştır.\n\nTelefon: {obj.phone}\nE-posta: {obj.email}',
                'noreply@avrasya.edu.tr',
                [request.user.email],
                fail_silently=True,
            )
        self.message_user(request, f'{queryset.count()} talep için hatırlatma e-postası gönderildi.')
    send_reminder_email.short_description = 'Seçili talepler için hatırlatma e-postası gönder'