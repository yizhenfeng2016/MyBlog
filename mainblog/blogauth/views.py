#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import (base36_to_int, is_safe_url,
                               urlsafe_base64_decode, urlsafe_base64_encode)
from blogauth.forms import BlogUserForm
from blogauth.models import BlogUser
from blogsystem.models import *
from blogsystem.forms import *
from blog.models import *

import time
import datetime
from PIL import Image
import os
import json
import base64
import logging

# logger = logging.getLogger(__name__)
# Create your views here.

class UserManage(View):
    def post(self, request, *args, **kwargs):
        #获取要对用户进行什么操作
        slug = self.kwargs.get('slug')
        if slug == 'login':
            return self.login(request)
        elif slug == "logout":
            return self.logout(request)
        elif slug == "register":
            return self.register(request)
        elif slug == "changepassword":
            return self.changepassword(request)
        elif slug == "forgetpassword":
            return self.forgetpassword(request)
        elif slug == "saveimage":
            return self.saveimage(request)
        elif slug == "resetpassword":
            return self.resetpassword(request)
        elif slug == "notification":
            return self.notification(request)
        elif slug == "sendmessage":
            return self.sendmessage(request)
        elif slug == "addcatagory":
            return self.addcatagory(request)
        elif slug == "addtag":
            return self.addtag(request)
        elif slug == "userinfo":
            return self.userinfo(request)
        else:
            raise PermissionDenied

    def get(self, request, *args, **kwargs):
        # 如果是get请求直接返回404页面
        raise Http404

    def login(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        print("username:",username)
        print("password:",password)
        user = auth.authenticate(username=username, password=password)

        errors = []

        if user is not None:
            auth.login(request, user)
        else:
            errors.append(u"密码或者用户名不正确")

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def logout(self, request):
        if not request.user.is_authenticated():
            # logger.error(u'[UserManage]用户未登陆')
            raise PermissionDenied
        else:
            auth.logout(request)
            return HttpResponse('OK')

    def register(self, request):
        username = self.request.POST.get("username", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")
        email = self.request.POST.get("email", "")

        form = BlogUserForm(request.POST)

        errors = []
        # 验证表单是否正确
        if form.is_valid():
            current_site = get_current_site(request)
            print(current_site)
            site_name = current_site.name
            domain = current_site.domain
            title = u"欢迎来到 {} ！".format(site_name)
            message = "".join([
                u"你好！ {} ,感谢注册 {} ！\n\n".format(username, site_name),
                u"请牢记以下信息：\n",
                u"用户名：{}\n".format(username),
                u"邮箱：{}\n".format(email),
                u"网站：http://{}\n\n".format(domain),
            ])
            from_email ="13592895405@163.com"
            try:
                send_mail(title, message, from_email, [email])
            except Exception as e:
                print(e.message)
                # logger.error(
                #     u'[UserManage]用户注册邮件发送失败:[{}]/[{}]'.format(
                #         username, email
                #     )
                # )
                return HttpResponse(u"发送邮件错误!\n注册失败", status=500)

            new_user = form.save()
            user = auth.authenticate(username=username, password=password2)
            auth.login(request, user)

        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def notification(self, request):
        if not request.user.is_authenticated():
            # logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied

        notification_id = self.request.POST.get("notification_id", "")
        notification_id = int(notification_id)
        print(notification_id)
        notification = Message.objects.filter(
            pk=notification_id  #pk就是Django模型类都有一个主键字段(ID)
        ).first()

        if notification:
            notification.is_read = True
            notification.save()
            mydict = {
                "context": notification.message_text.text,
                'title':notification.message_text.title
                }
            print(mydict)
        else:
            mydict = {
                "context": '',
                "title":''
                }

        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def sendmessage(self,request):
        if not request.user.is_authenticated():
            # logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied

        #获取表单数据
        to_user=request.POST.get("to_user","")
        message_title=request.POST.get("message_title","")
        message_text=request.POST.get("message_text","")
        form=SendMessageForm(request.POST)
        errors=[] #保存错误，传递回前端显示
        #在表单中验证收件人是否在用户数据库中
        if form.is_valid():
            dict_data={
                "title":message_title,
                "text":message_text,
                "message_type":0,
                "from_user":request.user
            }
            m=MessageText.objects.create(**dict_data)
            to_user=BlogUser.objects.get(username=to_user)
            dict_data={
                "is_read":0,
                "message_text":m,
                "to_user":to_user
                    }
            Message.objects.create(**dict_data)
        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def changepassword(self,request):
        if not request.user.is_authenticated():
            raise PermissionDenied

        form = PasswordChangeForm(request.user, request.POST) #采用系统的改密码表单

        errors = []
        # 验证表单是否正确
        if form.is_valid():
            user_forms = form.save()
            auth.logout(request) #退出登录
        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def addcatagory(self,request):
        if not request.user.is_authenticated():
            raise PermissionDenied
         #获取表单数据
        catagory_name=request.POST.get("catagory_name","")
        errors=[] #保存错误，传递回前端显示
        mydict2={}
        if catagory_name:
            dict_data={
                "name":catagory_name,
                "user":request.user
            }
            Catagory.objects.create(**dict_data)
            catagory=Catagory.objects.filter(name=catagory_name).last()
            mydict2 = {"id": catagory.id,"name":catagory.name}
        else:
            errors.append("名称未填")
        mydict = {"errors": errors}
        mydict.update(mydict2)
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def addtag(self,request):
        if not request.user.is_authenticated():
            raise PermissionDenied
         #获取表单数据
        tag_name=request.POST.get("tag_name","")
        errors=[] #保存错误，传递回前端显示
        mydict2={}
        if tag_name:
            dict_data={
                "name":tag_name,
                "user":request.user
            }
            Tag.objects.create(**dict_data)
            tag=Tag.objects.filter(name=tag_name).last()
            mydict2 = {"id": tag.id,"name":tag.name}
        else:
            errors.append("名称未填")

        mydict = {"errors": errors}
        mydict.update(mydict2)
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def saveimage(self,request):
        if not request.user.is_authenticated():
             raise PermissionDenied
         # 本地保存头像
        data = request.POST['image']
        #print(data)
        if not data:
            return HttpResponse(u"上传头像错误", status=500)

        imgdata = base64.b64decode(data)
        #print(imgdata)
        filename = "image_100x100_{}.jpg".format(request.user.id)
        filedir = "static/blog/user/"
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if static_root:
            filedir = os.path.join(static_root, 'userimage')
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        path = os.path.join(filedir, filename)
        with open(path,'wb+') as file:
            print("come in write img")
            file.write(imgdata)
            file.flush()

        # 修改头像分辨率
        try:
            im = Image.open(path).convert('RGB')
            out = im.resize((100, 100), Image.ANTIALIAS)
            out.save(path)
        except Exception as e:
            print(e.message)

        return HttpResponse(u"上传头像成功!")

    def userinfo(self,request):
        if not request.user.is_authenticated():
             raise PermissionDenied
        user=self.request.user
        nickname=request.POST["user_nickname"] #从name属性获取,也就是说html必须要有name字段
        province=request.POST["province"]
        city=request.POST["city"]
        sex=request.POST["sex"]
        intro=request.POST["user-message"]
        print(nickname)
        user.nickname=nickname
        user.province=province
        user.city=city
        user.sex=sex
        user.intro=intro

        filename = "image_100x100_{}.jpg".format(user.id)
        filedir = "static/blog/user/"
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if static_root:
            filedir = os.path.join(static_root, 'userimage')
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        path = os.path.join(filedir, filename)
        print(path)
        if os.path.exists(path):
            url=os.path.join("userimage",filename)
            print(url)
            user.img=url
        user.save()
        print("userinfo save success")
        return HttpResponseRedirect('/index')