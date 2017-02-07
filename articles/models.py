import string
from random import choice

import markdown2
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.db import models
from django.utils.text import slugify

from articles.constants import ARTICLE_CATEGORY_CHOICES


def unique_id(length=5):
    uid = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(length))
    if not Article.objects.filter(uid=uid).exists():
        return uid
    else:
        return unique_id()


class Article(models.Model):
    uid = models.CharField('Unique ID', primary_key=True, editable=False, max_length=5, default=unique_id)

    title = models.CharField('标题', max_length=255)
    slug = models.SlugField('slug', max_length=255, blank=True)

    author = models.ForeignKey(verbose_name='作者', to=settings.AUTH_USER_MODEL)

    category = models.CharField('目录', choices=ARTICLE_CATEGORY_CHOICES, max_length=16)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now_add=True)

    content = models.TextField('Markdown 文本')

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Only set the slug when the object is created.
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return '/a/%s/' % self.slug

    @property
    def markdown_content(self):
        return markdown2.markdown(self.content)

    def digest(self, size=140):
        content = self.content
        if len(content.split('\n')) > 8:
            content = ''.join(content.split('\n')[:8])
        if len(content) > size:
            content = content[:size]
        return content + ' ... '

    def digest_html(self, size=140):
        return markdown2.markdown(self.digest(size))

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
