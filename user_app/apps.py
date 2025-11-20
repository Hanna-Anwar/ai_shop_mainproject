from django.apps import AppConfig


class UserAappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'

    def ready(self):
        import user_app.signals
