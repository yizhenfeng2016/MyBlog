# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='catagory',
            name='smarthome',
            field=models.ForeignKey(related_name='catagory_user_set', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u7528\u6237'),
        ),
        migrations.AddField(
            model_name='tag',
            name='smarthome',
            field=models.ForeignKey(related_name='tag_user_set', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u7528\u6237'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(related_name='blog_author_set', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u4f5c\u8005'),
        ),
    ]
