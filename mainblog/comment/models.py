# coding:utf8
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from blog.models import Blog
from mainblog import settings

class Comment(models.Model):
    """
    评论
    """
    blog = models.ForeignKey(Blog,verbose_name='博客')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                null=True, blank=True,
                                related_name='from_user_comment_set',
                                verbose_name=u'评论者')
    # email = models.EmailField(verbose_name='邮箱')
    content = models.TextField(verbose_name='评论')
    reply_count=models.PositiveIntegerField(default=0)
    # content = models.CharField('内容',max_length=240)
    #content=RichTextUploadingField(verbose_name='评论', config_name='comment')
    created = models.DateTimeField('发布时间',auto_now_add=True)

    def __unicode__(self):
        return self.content

class ReplyComment(models.Model):
    """
    回复评论
    """
    blog=models.ForeignKey(Blog,verbose_name='博客')#一对多关系
    comment = models.ForeignKey(Comment,verbose_name='评论') #一对多关系
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                null=True, blank=True,
                                related_name='from_user_replycomment_set',
                                verbose_name=u'回复者')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                null=True, blank=True,
                                related_name='to_user_replycomment_set',
                                verbose_name=u'被回复者')
    # email = models.EmailField(verbose_name='邮箱',null=True,blank=True)#null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
                                                               #blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填，比如 admin 界面下增加 model 一条记录的时候。直观的看到就是该字段不是粗体
    content = models.TextField(verbose_name='回复')
    # content = models.CharField('内容',max_length=240)
    #content=RichTextUploadingField(verbose_name='评论', config_name='comment')
    created = models.DateTimeField('发布时间',auto_now_add=True)

    def __unicode__(self):
        return self.content

class Count(models.Model):
    "阅读数、评论数"
    blog=models.OneToOneField(Blog,on_delete=models.CASCADE,primary_key=True)
    readed=models.IntegerField(default=0)
    commented=models.IntegerField(default=0)
