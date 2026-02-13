# fen_edebiyat/apps.py
from django.apps import AppConfig

class FenEdebiyatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fen_edebiyat'
    verbose_name = 'Fen Edebiyat Fakültesi'
    
    def ready(self):
        import fen_edebiyat.signals