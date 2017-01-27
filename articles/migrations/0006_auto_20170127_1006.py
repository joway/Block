# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-27 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
    ]