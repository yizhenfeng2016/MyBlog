# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SmartHomeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('password', models.CharField(max_length=20, verbose_name='\u5bc6\u7801')),
                ('token', models.CharField(max_length=200, verbose_name='Token')),
            ],
        ),
    ]
