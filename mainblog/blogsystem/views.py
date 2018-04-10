# -*- coding: utf-8 -*-
from django import template
from django import forms
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.template import Context, loader
from django.views.generic import View, TemplateView, ListView, DetailView
from django.db.models import Q
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
# from blog.models import Article, Category, Carousel, Column, Nav, News
# from vmaig_comments.models import Comment
from blogauth.models import BlogUser
from blogsystem.models import *
from blogsystem.forms import *
from blogauth.forms import BlogUserForm
from django.conf import settings
import datetime
import time
import json
import logging

# 缓存
# try:
#     cache = caches['memcache']
# except ImportError as e:
#     cache = caches['default']

# logger
# logger = logging.getLogger(__name__)

class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 网站标题等内容
            # context['website_title'] = settings.WEBSITE_TITLE
            # context['website_welcome'] = settings.WEBSITE_WELCOME
            # 热门文章
            # context['hot_article_list'] = \
            #     Article.objects.order_by("-view_times")[0:10]
            # # 导航条
            # context['nav_list'] = Nav.objects.filter(status=0)
            # # 最新评论
            # context['latest_comment_list'] = \
            #     Comment.objects.order_by("-create_time")[0:10]
            # # 友情链接
            context['links'] = Link.objects.order_by('create_time').all()
            colors = ['primary', 'success', 'info', 'warning', 'danger']
            for index, link in enumerate(context['links']):
                link.color = colors[index % len(colors)]
            # 用户未读消息数
            user = self.request.user
            if user.is_authenticated():
                context['notification_count'] = \
                    user.to_user_notification_set.filter(is_read=0).count()
        except Exception as e:

            print(e.message)

        return context

class UserView(BaseMixin, TemplateView):
    template_name = 'user-notification.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, 'user-notification.html')
        slug = self.kwargs.get('slug')

        if slug == 'userinfo':
            self.template_name = 'user-info.html'
        elif slug == 'changepassword':
            self.template_name = 'user-changepassword.html'
        # elif slug == 'changeinfo':
        #     self.template_name = 'smarthome-changeinfo.html'
        # elif slug == 'message':
        #     self.template_name = 'smarthome-message.html'
        elif slug == 'notification':
            self.template_name = 'user-notification.html'
        elif slug =='sendmessage':
            self.template_name='user_send_message.html'
        else:

            raise Http404
        return super(UserView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        slug =self.kwargs.get('slug')
        if slug == 'notification':
            global_message_objext_list=MessageText.objects.filter(message_type=1) #获取所有系统信息
            #插入系统消息
            for m in global_message_objext_list:
                try:
                    self.request.user.to_user_notification_set.get(message_text_id=m.id)
                except Message.DoesNotExist:
                    dict_data={
                        "is_read":0,
                        "message_text":m,
                        "to_user":self.request.user,
                    }
                    Message.objects.create(**dict_data)
            #获取推送给这个用户的所有消息
            context['notifications'] = self.request.user.to_user_notification_set.order_by("-message_text_id").all()

        # elif slug=='sendmessage':
        #     mf=SendMessageForm()
        #     context['mf']=mf
        # elif slug=='userinfo':


        return context

