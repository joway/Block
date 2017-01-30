from django.apps import AppConfig
from django.contrib import algoliasearch


class ArticlesConfig(AppConfig):
    name = 'articles'

    def ready(self):
        from actstream import registry
        article = self.get_model('Article')
        algoliasearch.register(article)
        registry.register(article)
