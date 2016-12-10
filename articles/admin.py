from django.contrib import admin

from articles.forms import ArticleModelForm
from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['uid', 'title', 'tag_list', 'author']
    form = ArticleModelForm

    class Meta:
        model = Article

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Article, ArticleAdmin)
