#-*- coding:utf-8 -*-
__author__ = 'Administrator'

from django.conf.urls import url
from blogauth.views import UserManage
from mainblog.settings import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
        url(r'^user/(?P<slug>\w+)$', UserManage.as_view()), #处理post信息
        url(r'^static/(?P<path>(\S)*)','django.views.static.serve',{'document_root':BASE_DIR+'\static'}),
]
