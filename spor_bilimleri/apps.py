# spor_bilimleri/apps.py
from django.apps import AppConfig

class SporBilimleriConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spor_bilimleri'
    verbose_name = 'Spor Bilimleri Fakültesi'
    
    def ready(self):
        import spor_bilimleri.signals