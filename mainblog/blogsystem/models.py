# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# Create your models here.


IS_READ = {
    0: u'未读',
    1: u'已读'
}

MESSAGE_TYPE={
    0:u'私信',
    # 1:u"公共消息",
    1:u"系统消息"
}

class MessageText(models.Model):
    #ID：编号；SendID：发送者编号；Message：站内信的内容；Type:信息类型；Group:用户组ID;  PostDate：站内信发送时间
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  default=None, blank=True, null=True,
                                  related_name='from_user_notification_set',
                                  verbose_name=u'发送者')
    title = models.CharField(max_length=100, verbose_name=u'标题')
    text = models.TextField(verbose_name=u'内容')
    message_type= models.IntegerField(default=0, choices=MESSAGE_TYPE.items(),
                                  verbose_name=u'信息类型')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'消息'
        ordering = ['-create_time']

class Message(models.Model):
    #ID：编号；RecID：接收者编号;MessageID：站内信编号；Statue：站内信的查看状态
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='to_user_notification_set',
                                verbose_name=u'接收者')
    is_read = models.IntegerField(default=0, choices=IS_READ.items(),
                                  verbose_name=u'是否读过')
    message_text=models.ForeignKey(MessageText,
                                   related_name='message_text_set',
                                   verbose_name=u'信息内容')

# class Notification(models.Model):
#     title = models.CharField(max_length=100, verbose_name=u'标题')
#     text = models.TextField(verbose_name=u'内容')
#     url = models.CharField(max_length=200, verbose_name=u'连接',
#                            null=True, blank=True)
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                   default=None, blank=True, null=True,
#                                   related_name='from_user_notification_set',
#                                   verbose_name=u'发送者')
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                 related_name='to_user_notification_set',
#                                 verbose_name=u'接收者')
#     type = models.CharField(max_length=20, verbose_name=u'类型',
#                             null=True, blank=True)
#
#     is_read = models.IntegerField(default=0, choices=IS_READ.items(),
#                                   verbose_name=u'是否读过')
#
#     create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
#     update_time = models.DateTimeField(u'更新时间', auto_now=True)

    # class Meta:
    #     verbose_name_plural = verbose_name = u'消息'
    #     ordering = ['-create_time']


class Link(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    url = models.CharField(max_length=200, verbose_name=u'连接',
                           null=True, blank=True)
    type = models.CharField(max_length=20, verbose_name=u'类型',
                            null=True, blank=True)

    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = u'友情链接'
        ordering = ['-create_time']
