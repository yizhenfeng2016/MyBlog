#-*- coding:utf-8 -*-
__author__ = 'Administrator'

from django.conf.urls import url
from blogsystem.views import UserView
from django.views.generic import TemplateView

urlpatterns = [
        url(r'^userview/(?P<slug>\w+)$', UserView.as_view(), name='user-view'), #处理用户模板
        url(r'^login/$',
            TemplateView.as_view(template_name="user-login.html"),
            name='login-view'),
        # url(r'',
        #     TemplateView.as_view(template_name="user-login.html"),
        #     name='login-view'),
        url(r'^register/$',
            TemplateView.as_view(template_name="user-register.html"),
            name='register-view'),
 ]