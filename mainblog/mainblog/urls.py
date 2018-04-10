# coding=utf-8

from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls import url,include,patterns
from django.contrib import admin
from blog.views import *
from mainblog.settings import *
from comment.views import *

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls,name='blog_admin'),
    url(r'',include("blog.urls")),
    url(r'',include("blogauth.urls")),
    url(r'',include("blogsystem.urls")),
	url(r'',include("smarthome.urls")),
    url(r'',get_all_blogs,name='get_all_blogs'),
  ]
