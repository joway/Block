from django.contrib.algoliasearch import AlgoliaIndex


class ArticleAlgoliaIndex(AlgoliaIndex):
    tags = 'category'
    fields = ('title', 'content')
    settings = {'attributesToIndex': ['title', 'content']}
    index_name = 'article_index'
