# coding:utf8
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from mainblog import settings

# Create your models here.
class Catagory(models.Model):
    """
    博客分类
    """
    name = models.CharField('名称',max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  default=None, blank=True, null=True,
                                  related_name='catagory_user_set',
                                  verbose_name=u'用户')

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    """
    博客标签
    """
    name = models.CharField('名称',max_length=16)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  default=None, blank=True, null=True,
                                  related_name='tag_user_set',
                                  verbose_name=u'用户')

    def __unicode__(self):
        return self.name

class Blog(models.Model):
    """
    博客
    """
    title = models.CharField('标题',max_length=32)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  default=None, blank=True, null=True,
                                  related_name='blog_author_set',
                                  verbose_name=u'作者')
    # content = models.TextField('博客正文')
    content = RichTextField('博客正文',config_name='default')
    created = models.DateTimeField('发布时间',auto_now_add=True)
    catagory = models.ForeignKey(Catagory,verbose_name='分类')
    tags = models.ManyToManyField(Tag,verbose_name='标签')

    def __unicode__(self):
        return self.title






