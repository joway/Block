# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-07 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialaccount',
            name='provider',
            field=models.IntegerField(choices=[(1, 'Github'), (2, 'QQ'), (3, 'Coding')], verbose_name='类别'),
        ),
    ]