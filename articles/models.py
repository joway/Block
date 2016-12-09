from activity.services import ActivityService
from catalog.models import Catalog
from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
from utils.constants import ContentTypes


class Article(models.Model):
    title = models.CharField('标题', max_length=255)
    author = models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL)
    content = models.TextField('Markdown 文本')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now_add=True)

    tags = TaggableManager(blank=True)

    catalog = models.ForeignKey(verbose_name='目录', to=Catalog)

    def tag_list(self):
        return [o.name for o in self.tags.all()]

    def comment_list(self):
        return comment.services.CommentService.get_comments(comment_to=self.id, type=ContentTypes.ARTICLE)

    def save(self, *args, **kwargs):
        super(...).save(*args, **kwargs)
        ActivityService.create_activity(user=self.author, obj=self, type=ContentTypes.ARTICLE)
