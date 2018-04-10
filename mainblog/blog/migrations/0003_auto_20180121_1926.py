# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_auto_20180111_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catagory',
            name='smarthome',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='smarthome',
        ),
        migrations.AddField(
            model_name='catagory',
            name='user',
            field=models.ForeignKey(related_name='catagory_user_set', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u7528\u6237'),
        ),
        migrations.AddField(
            model_name='tag',
            name='user',
            field=models.ForeignKey(related_name='tag_user_set', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u7528\u6237'),
        ),
    ]
