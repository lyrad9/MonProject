from django.apps import AppConfig


class GestionServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Gestion_Service'

    def ready(self):
        from . import signals  # 👈 Importer les signaux ici
