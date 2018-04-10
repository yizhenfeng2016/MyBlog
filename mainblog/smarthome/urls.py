#-*- coding:utf-8 -*-
__author__ = 'Administrator'

from django.conf.urls import url
from django.views.generic import TemplateView
from smarthome.views import *

urlpatterns = [
        url(r'^smarthome/$',
            TemplateView.as_view(template_name="smarthome.html"),
            name='smarthome_get_msg'),
        url(r'^smarthome/control/$',TemplateView.as_view(template_name="smarthome-control.html"),name='smarthome_control'),
        url(r'^smarthome/login/$',smarthome_login,name='smarthome_login'),
        url(r'^smarthome/bind/$', TemplateView.as_view(template_name="smarthome-bind.html"),
            name='smarthome_bind'),
        url(r'^smarthome/register/$', TemplateView.as_view(template_name="smarthome-register.html"),
            name='smarthome_register'),
        url(r'^smarthome/forgetpassword/$', TemplateView.as_view(template_name="smarthome-forgetpwd.html"),
            name='smarthome_forgetpwd'),
        url(r'^smarthome/update/(?P<slug>\w+)$', UpdateInfo.as_view()), #处理post信息
 ]