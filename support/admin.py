from django.contrib import admin
from .models import Category, Department, FAQ, Ticket, TicketReply


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'department')
    search_fields = ('question',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'department', 'status', 'created_at')
    list_filter = ('status', 'department')
    search_fields = ('subject', 'message')


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'staff', 'created_at')
    search_fields = ('message', 'staff__username')



