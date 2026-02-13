from django.apps import AppConfig

class LeeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lee'
    verbose_name = 'lee'
    
    def ready(self):
        import lee.signals