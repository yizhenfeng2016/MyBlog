# coding:utf-8
from django import forms
from blog.models import Blog

#定义Blog模型
class BlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=('title','author','content')