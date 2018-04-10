# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
        migrations.RemoveField(
            model_name='replycomment',
            name='name',
        ),
        migrations.AddField(
            model_name='comment',
            name='from_user',
            field=models.ForeignKey(related_name='from_user_comment_set', verbose_name='\u8bc4\u8bba\u8005', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='replycomment',
            name='from_user',
            field=models.ForeignKey(related_name='from_user_replycomment_set', verbose_name='\u56de\u590d\u8005', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='replycomment',
            name='to_user',
            field=models.ForeignKey(related_name='to_user_replycomment_set', verbose_name='\u88ab\u56de\u590d\u8005', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
