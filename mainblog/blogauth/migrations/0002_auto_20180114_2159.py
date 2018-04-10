# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloguser',
            name='city',
            field=models.CharField(max_length=100, null=True, verbose_name='\u57ce\u5e02', blank=True),
        ),
        migrations.AddField(
            model_name='bloguser',
            name='nickname',
            field=models.CharField(max_length=100, null=True, verbose_name='\u6635\u79f0', blank=True),
        ),
        migrations.AddField(
            model_name='bloguser',
            name='province',
            field=models.CharField(max_length=100, null=True, verbose_name='\u7701\u4efd', blank=True),
        ),
        migrations.AddField(
            model_name='bloguser',
            name='sex',
            field=models.IntegerField(default=0, verbose_name='\u6027\u522b', choices=[(0, b'\xe4\xbf\x9d\xe5\xaf\x86'), (1, b'\xe7\x94\xb7'), (2, b'\xe5\xa5\xb3')]),
        ),
        migrations.AlterField(
            model_name='bloguser',
            name='img',
            field=models.CharField(default=b'/static/userimage/default.jpg', max_length=200, verbose_name='\u5934\u50cf\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='bloguser',
            name='intro',
            field=models.CharField(max_length=200, null=True, verbose_name='\u4e2a\u6027\u7b7e\u540d', blank=True),
        ),
    ]
