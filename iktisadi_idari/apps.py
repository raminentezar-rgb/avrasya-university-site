# iktisadi_idari/apps.py
from django.apps import AppConfig

class IktisadiIdariConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iktisadi_idari'
    verbose_name = 'İktisadi ve İdari Bilimler Fakültesi'
    
    def ready(self):
        import iktisadi_idari.signals