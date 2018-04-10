#coding:utf-8
from django.db import models

# Create your models here.

class SmartHomeUser(models.Model):
    username=models.CharField(max_length=20,
                             verbose_name=u'手机号码')
    password=models.CharField(max_length=20,
                             verbose_name=u'密码')
    token=models.CharField(max_length=200,
                             verbose_name=u'Token')