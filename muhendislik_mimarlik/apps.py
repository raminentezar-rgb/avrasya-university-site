# muhendislik_mimarlik/apps.py
from django.apps import AppConfig

class MuhendislikMimarlikConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'muhendislik_mimarlik'
    verbose_name = 'Mühendislik ve Mimarlık Fakültesi'
    
    def ready(self):
        import muhendislik_mimarlik.signals