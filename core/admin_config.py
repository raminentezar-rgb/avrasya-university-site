from django.contrib import admin


def configure_admin_site():
    """Apply user-friendly Turkish branding to Django's default AdminSite."""
    admin.site.site_header = "Avrasya Üniversitesi"
    admin.site.site_title = "Avrasya Üniversitesi Yönetim Paneli"
    admin.site.index_title = "İçerik Yönetim Merkezi"
