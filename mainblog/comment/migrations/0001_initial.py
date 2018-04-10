# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16, verbose_name='\u79f0\u547c')),
                ('email', models.EmailField(max_length=254, verbose_name='\u90ae\u7bb1')),
                ('content', models.TextField(verbose_name='\u8bc4\u8bba')),
                ('reply_count', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('blog', models.OneToOneField(primary_key=True, serialize=False, to='blog.Blog')),
                ('readed', models.IntegerField(default=0)),
                ('commented', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16, verbose_name='\u79f0\u547c')),
                ('content', models.TextField(verbose_name='\u56de\u590d')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('blog', models.ForeignKey(verbose_name='\u535a\u5ba2', to='blog.Blog')),
                ('comment', models.ForeignKey(verbose_name='\u8bc4\u8bba', to='comment.Comment')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(verbose_name='\u535a\u5ba2', to='blog.Blog'),
        ),
    ]
