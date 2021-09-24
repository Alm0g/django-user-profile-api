from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self) -> None:
        """
        Override this method in subclasses to run code when Django starts.
        """
        import profiles.signals
