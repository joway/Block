import string
from random import choice

import markdown2
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.db import models
from taggit.managers import TaggableManager

from articles.constants import ARTICLE_CATEGORY_CHOICES
from articles.tag import ArticleTaggedItem


def unique_id(length=5):
    uid = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(length))
    if not Article.objects.filter(uid=uid).exists():
        return uid
    else:
        return unique_id()


class Article(models.Model):
    uid = models.CharField('Unique ID', primary_key=True, editable=False, max_length=5, default=unique_id)

    title = models.CharField('标题', max_length=255)
    author = models.ForeignKey(verbose_name='作者', to=settings.AUTH_USER_MODEL)

    content = models.TextField('Markdown 文本')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now_add=True)

    tags = TaggableManager(blank=True, through=ArticleTaggedItem)

    category = models.CharField('目录', choices=ARTICLE_CATEGORY_CHOICES, max_length=16)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return '/a/%s/' % self.uid

    def tag_list(self):
        return [o.name for o in self.tags.all()]

    @property
    def markdown_content(self):
        return markdown2.markdown(self.content)

    @property
    def digest(self):
        return self.content[:140] + '...'

    @property
    def url(self):
        return '/a/%s/' % self.uid

    def __str__(self):
        return self.title


class ArticleRSSFeed(Feed):
    title = "城西笔谈 - 文章列表"
    link = "/"
    description = "城西笔谈 - blog posts"

    def items(self):
        return Article.objects.order_by('-created_at')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.created_at

    def item_description(self, item):
        return item.markdown_content
