# coding:utf-8
from django import forms
from comment.models import Comment

"""
借此实现博客的评论功能
"""
# class CommentForm(forms.ModelForm):
#     #自定义modelForm的内容
#     class Meta:
#         model=Comment
#         fields=('name','email','content')

class CommentForm(forms.Form):
    """
    评论表单用于发表博客的评论。评论表单的类并根据需求定义了字段：评论内容。这样我们就能利用它来快速生成表单并验证用户的输入。
    """
    content = forms.CharField(label='评论内容',error_messages={
        'required':'请填写您的评论内容！',
        'max_length':'评论内容太长咯'
    })
