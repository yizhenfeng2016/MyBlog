#-*- coding:utf-8 -*-

from django import forms
from blogsystem.models import Message,MessageText
from blogauth.models import BlogUser

#定义表单模型
class SendMessageForm(forms.Form):
    # 错误信息
    error_messages = {
        'username_no_exit': u"此用户不存在."
    }

    # 错误信息 invalid 表示username不合法的错误信息,
    # required 表示没填的错误信息
    to_user = forms.CharField(
        label='收件人',
        max_length=30,
        error_messages={
            'invalid':  u"该值只能包含字母、数字和字符@/./+/-/_",
            'required': u"用户名未填"
        }
    )
    message_title = forms.CharField(
        label='标题',
        max_length=100,
        error_messages={
            'required': u"标题未填"
            }
    )
    message_text = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.Textarea,
        error_messages={
            'required': u"内容未填"
            }
    )

    def clean_to_user(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        to_user = self.cleaned_data["to_user"]
        try:
            BlogUser._default_manager.get(username=to_user)
        except BlogUser.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages["username_no_exit"]
        )