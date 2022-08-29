from django.apps import AppConfig

class MultisessionManagerCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pullgerMultisessionManager_REST'
    multisessionManager = None