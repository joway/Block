from django.apps import AppConfig
from django.contrib import algoliasearch
from django.contrib.algoliasearch import AlgoliaIndex


class ArticleIndex(AlgoliaIndex):
    fields = ('title', 'content', 'category')
    settings = {'attributesToIndex': ['title', 'content']}
    index_name = 'article_index'


class ArticlesConfig(AppConfig):
    name = 'articles'

    def ready(self):
        from actstream import registry
        article = self.get_model('Article')
        algoliasearch.register(article, ArticleIndex)
        registry.register(article)
