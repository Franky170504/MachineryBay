from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = 'Customer Management'
    
    def ready(self):
        """
        Import signals when Django starts.
        """
        import users.signals  # noqa
