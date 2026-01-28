from django.contrib import admin
from .models import ResearchPolicy, BAPProject, Laboratory, ResearchCenter, IntellectualProperty, ResearchOutput, Award

@admin.register(ResearchPolicy)
class ResearchPolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'commission', 'order', 'is_active']

@admin.register(BAPProject)
class BAPProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'coordinator', 'budget', 'status']

@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'faculty', 'director', 'is_active']

# # مدل‌های جدید را موقتاً کامنت کنید
@admin.register(ResearchCenter)
class ResearchCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'director', 'faculty', 'status', 'researcher_count']
    list_filter = ['status', 'faculty']
    search_fields = ['name', 'director']

@admin.register(IntellectualProperty)
class IntellectualPropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'inventor', 'status', 'registration_date']
    list_filter = ['property_type', 'status', 'is_international']
    search_fields = ['title', 'inventor', 'registration_number']

@admin.register(ResearchOutput)
class ResearchOutputAdmin(admin.ModelAdmin):
    list_display = ['title', 'output_type', 'publication_date', 'citation_count', 'impact_factor']
    list_filter = ['output_type', 'quartile']
    search_fields = ['title', 'authors', 'journal']
    date_hierarchy = 'publication_date'

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['title', 'award_type', 'recipient', 'award_date', 'is_featured']
    list_filter = ['award_type', 'is_featured']
    search_fields = ['title', 'recipient', 'awarding_organization']