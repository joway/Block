from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'articles'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Article'))
