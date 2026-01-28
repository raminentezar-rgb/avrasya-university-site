# meslek_yuksekokulu/apps.py
from django.apps import AppConfig

class MeslekYuksekokuluConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meslek_yuksekokulu'
    verbose_name = 'Meslek Yüksekokulu'
    
    def ready(self):
        import meslek_yuksekokulu.signals