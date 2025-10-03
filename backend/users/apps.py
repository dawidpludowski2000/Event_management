from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        import users.signals.send_activation_email  # noqa: F401
        print("[UsersConfig.ready] signals imported OK")
