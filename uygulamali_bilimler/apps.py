# uygulamali_bilimler/apps.py
from django.apps import AppConfig

class UygulamaliBilimlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uygulamali_bilimler'
    verbose_name = 'Uygulamalı Bilimler'
    
    def ready(self):
        import uygulamali_bilimler.signals