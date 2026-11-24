from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .admin_config import configure_admin_site
        from .signals import connect_cache_invalidation_signals
        configure_admin_site()
        connect_cache_invalidation_signals()
