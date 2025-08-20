from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


    def ready(self):
        print("[UsersConfig.ready] start")
        import users.signals.send_activation_email
        print("[UsersConfig.ready] signals imported")