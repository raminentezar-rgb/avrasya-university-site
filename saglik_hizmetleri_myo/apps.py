# saglik_hizmetleri_myo/apps.py
from django.apps import AppConfig

class SaglikHizmetleriMYOConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saglik_hizmetleri_myo'
    verbose_name = 'Sağlık Hizmetleri Meslek Yüksekokulu'
    
    def ready(self):
        import saglik_hizmetleri_myo.signals