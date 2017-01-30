from django.contrib import admin

from articles.forms import ArticleModelForm
from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['uid', 'title', 'category', 'created_at']
    form = ArticleModelForm

    class Meta:
        model = Article

admin.site.register(Article, ArticleAdmin)
