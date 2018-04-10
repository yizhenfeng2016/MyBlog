# coding:utf8
from django.contrib import admin

# Register your models here.
from comment.models import *
# 注册的目的就是为了让系统管理员能对注册的这些模型进行管理
admin.site.register([Comment,ReplyComment,Count])