# saglik_bilimleri/apps.py
from django.apps import AppConfig

class SaglikBilimleriConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saglik_bilimleri'
    verbose_name = 'Sağlık Bilimleri Fakültesi'
    
    def ready(self):
        import saglik_bilimleri.signals