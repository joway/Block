# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-30 12:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_article_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articletaggeditem',
            name='content_object',
        ),
        migrations.DeleteModel(
            name='ArticleTaggedItem',
        ),
    ]
