from django.apps import AppConfig, apps


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('User'))
        registry.register(apps.get_model('auth.Group'))
