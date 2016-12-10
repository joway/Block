from django.db import models
from taggit.models import Tag, ItemBase


class ArticleTaggedItem(ItemBase):
    tag = models.ForeignKey(Tag, related_name="%(app_label)s_%(class)s_tagged_items")

    # it supports string pk of content_object
    object_id = models.CharField(verbose_name='Object id', max_length=5, db_index=True)
    content_object = models.ForeignKey('articles.Article')

    @classmethod
    def tags_for(cls, model, instance=None):
        if instance is not None:
            return cls.tag_model().objects.filter(**{
                '%s__content_object' % cls.tag_relname(): instance
            })
        return cls.tag_model().objects.filter(**{
            '%s__content_object__isnull' % cls.tag_relname(): False
        }).distinct()
