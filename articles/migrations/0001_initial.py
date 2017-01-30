# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-15 12:35
from __future__ import unicode_literals

import articles.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('uid', models.CharField(default=articles.models.unique_id, editable=False, max_length=5, primary_key=True, serialize=False, verbose_name='Unique ID')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('content', models.TextField(verbose_name='Markdown 文本')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('category', models.CharField(choices=[('programing', '编程'), ('software', '软件'), ('thinking', '随想'), ('enviroment', '环境'), ('literature', '文艺')], max_length=16, verbose_name='目录')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleTaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(db_index=True, max_length=5, verbose_name='Object id')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Article')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
