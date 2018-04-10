#coding:utf-8
__author__ = 'Administrator'
from  django import forms

class SmartHomeUserForm(forms.ModelForm):
     username = forms.RegexField(
        max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid':  u"该值只能包含字母、数字和字符@/./+/-/_",
            'required': u"用户名未填"
        }
     )
     password= forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': u"密码未填"
            }
    )