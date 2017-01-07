from django.db import models


class Feed(models.Model):
    name = models.CharField('名称', max_length=255)
    homepage = models.CharField('主页', default='#', max_length=128)

    url = models.URLField('Feed 链接')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class FeedStream(models.Model):
    title = models.CharField('标题', max_length=255)
    author = models.CharField('作者', max_length=128)
    feed = models.ForeignKey(Feed, verbose_name='订阅')

    link = models.URLField('链接')
    content = models.TextField('内容')

    created_at = models.DateTimeField('创建时间', null=True, blank=True)
    indexed_at = models.DateTimeField('更新时间', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
