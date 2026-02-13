# iletisim/apps.py
from django.apps import AppConfig

class IletisimConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iletisim'
    verbose_name = 'İletişim ve Bilgi'
    
    def ready(self):
        import iletisim.signals