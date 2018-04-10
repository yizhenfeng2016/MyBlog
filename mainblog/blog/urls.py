#-*- coding:utf-8 -*-
__author__ = 'Administrator'

from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blog.views import *
from mainblog.settings import *

urlpatterns = [
    url(r'^index/',get_all_blogs,name='get_all_blogs'),
    url(r'^blogs/',get_user_blogs,name='get_user_blogs'),
    url(r'^blog/add/(\d+)/$',blog_add,name="blog_add_article"),
    url(r'^blog/modify/(\d+)/$',blog_modify,name="blog_modify_article"),
    url(r'^detail/(\d+)/$',get_details ,name='blog_get_detail'),
    url(r'^ckeditor/',include('ckeditor_uploader.urls')),
    url(r'^uploadimg/',upload_image),
    url(r'^upload/(?P<path>(\S)*)','django.views.static.serve',{'document_root':BASE_DIR+'\upload'}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #没有这一句无法显示上传的图片