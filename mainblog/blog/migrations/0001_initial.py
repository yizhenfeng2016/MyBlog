# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=32, verbose_name='\u6807\u9898')),
                ('author', models.CharField(max_length=16, verbose_name='\u4f5c\u8005')),
                ('content', ckeditor.fields.RichTextField(verbose_name='\u535a\u5ba2\u6b63\u6587')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u79f0')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16, verbose_name='\u540d\u79f0')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='catagory',
            field=models.ForeignKey(verbose_name='\u5206\u7c7b', to='blog.Catagory'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', verbose_name='\u6807\u7b7e'),
        ),
    ]
