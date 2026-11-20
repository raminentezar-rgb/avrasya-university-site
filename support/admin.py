from django.contrib import admin
from .models import (
    TicketReply, FAQ, Department, Ticket, Category,
    KnowledgeBase, Tag, ImportantLink,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'staff')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'department', 'is_active')
    list_filter = ('is_active', 'department')
    search_fields = ('question',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'subject', 'requester_name', 'requester_email', 'department', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority', 'department')
    search_fields = ('tracking_code', 'subject', 'message', 'guest_name', 'guest_email', 'user__username', 'user__email')
    readonly_fields = ('tracking_code', 'created_at', 'updated_at')


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'display_sender', 'is_staff_reply', 'created_at')
    list_filter = ('is_staff_reply',)
    search_fields = ('message', 'sender_name', 'staff__username', 'ticket__tracking_code')


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'category', 'department', 'views', 'updated_at')
    list_filter = ('content_type', 'department')
    search_fields = ('title', 'content')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ImportantLink)
class ImportantLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'category', 'order')
    search_fields = ('title', 'description')
