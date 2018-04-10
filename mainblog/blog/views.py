# coding:utf8
from webbrowser import Error

from django.shortcuts import render, render_to_response,RequestContext

# Create your views here.
import json
from blog.models import *
from comment.models import *
from comment.forms import CommentForm
from django.http import Http404,HttpResponse,HttpResponseRedirect

# from  templatetags.paginate_tags import paginate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage,InvalidPage
from blog.forms import BlogForm

# 获取博客列表
def get_all_blogs(request):
    blogs_list = Blog.objects.all().order_by('-created')
    after_range_num = 3        #当前页前显示2页
    befor_range_num = 2       #当前页后显示2页
    try:                     #如果请求的页码少于1或者类型错误，则跳转到第1页
        page = int(request.GET.get("page",1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(blogs_list,5)   # 设置books在每页显示的数量，这里为2
    try:                     #跳转到请求页面，如果该页不存在或者超过则跳转到尾页
        blogs = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        blogs = paginator.page(paginator.num_pages)
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+befor_range_num]
    for blog in blogs:
        try:
            Count.objects.get(blog_id=blog.id)
        except Count.DoesNotExist:
            c=Count(blog=blog,readed=0,commented=0)
            c.save()

    return render(request,'index.html', {'blogs': blogs,'page_range':page_range})

#获取某个用户的文章
def get_user_blogs(request):
    if not request.user.is_authenticated():
        return render(request, 'user-login.html')
    blogs_list = Blog.objects.filter(author=request.user).order_by('-created')
    after_range_num = 3        #当前页前显示2页
    befor_range_num = 2       #当前页后显示2页
    try:                     #如果请求的页码少于1或者类型错误，则跳转到第1页
        page = int(request.GET.get("page",1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(blogs_list,5)   # 设置books在每页显示的数量，这里为2
    try:                     #跳转到请求页面，如果该页不存在或者超过则跳转到尾页
        blogs = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        blogs = paginator.page(paginator.num_pages)
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+befor_range_num]
    for blog in blogs:
        try:
            Count.objects.get(blog_id=blog.id)
        except Count.DoesNotExist:
            c=Count(blog=blog,readed=0,commented=0)
            c.save()

    return render(request,'index.html', {'blogs': blogs,'page_range':page_range})


#添加、编辑、删除博客
def blog_add(request,blog_id):
    if not request.user.is_authenticated():
            return render(request, 'user-login.html')
    if request.method == "POST":
        if request.POST.has_key("save"):
            blogform= BlogForm(request.POST)
            if blogform.is_valid():
                #获取表单信息
                title= blogform.cleaned_data['title']
                # author= blogform.cleaned_data['author']
                author=request.user
                content= blogform.cleaned_data['content']
                catagory_id=request.POST['catagory']
                tags_id= request.REQUEST.getlist('tags')

                #将表单写入数据库
                print(type(blog_id))
                print(blog_id==0)
                print(blog_id=='0')
                if blog_id=='0':
                    blog= Blog()
                else:
                    blog=Blog.objects.get(id=blog_id)
                blog.title=title
                blog.author=author
                blog.content=content
                blog.catagory=Catagory.objects.get(id=catagory_id)
                #传进去的是列表，不是对象,是要创建对象后，然后再add添加tag
                blog.save()
                for tag_id in tags_id:
                    blog.tags.add(Tag.objects.get(id=tag_id))
                print("blog add success")
            return HttpResponseRedirect('/blogs/')
        else:
            blog=Blog.objects.get(id=blog_id)
            print(blog)
            blog.delete()
            print("blog delete success")
            return HttpResponseRedirect('/blogs/')

    elif  request.method=='GET':
        tags=request.user.tag_user_set.all() #查询用户的tag
        catagory=request.user.catagory_user_set.all()#查询用户的catagory
        ctx={
            "tags":tags,
            "catagory":catagory
        }
        return render(request,"article-add.html",ctx)

def blog_modify(request, blog_id):
    if not request.user.is_authenticated():
            return render(request, 'user-login.html')
    else:
        print(request.user)
        blog = Blog.objects.get(id=blog_id)
        if request.user==blog.author:
            print("get success")
            print(blog)
            tags=request.user.tag_user_set.all() #查询用户的tag
            catagory=request.user.catagory_user_set.all()#查询用户的catagory
            print(tags)
            print(catagory)
            ctx={
                "tags":tags,
                "catagory":catagory,
                "blog":blog
            }
            return render(request,"article-modify.html",ctx)
        else:
            print("user not true")
            return HttpResponseRedirect('/blogs/')

# 点击了博客列表中的某一项之后跳转到详情界面的方法以及评论
import datetime
def get_details(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
        # 获取对应的博客的所有的标签信息
        tags = blog.tags.all()
        try:
            Count.objects.get(blog_id=blog_id)
        except Count.DoesNotExist:
            print("come in except not exist")
            c=Count(blog=blog,readed=0,commented=0)
            c.save()
        count=blog.count
        print(count.commented)
        print(request.is_ajax())
    except Blog.DoesNotExist:
        raise Http404
    if request.is_ajax():
        print("come in ajax")
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({"errors":"请先登录，登录后才能发表评论！"}))
        content=request.POST.get('content',None)
        flag=request.POST.get('flag',None)
        if flag=="comment":
            print("flag:--comment")
            count.commented=count.commented+1
            count.save()
            if content:
                cleaned_data={"from_user":request.user,"content":content}
                cleaned_data['blog'] = blog #不能去掉，联系外键
                Comment.objects.create(**cleaned_data)
                new_comment_id=Comment.objects.values('id').last()['id']
                # new_comment=Comment.objects.get(id=new_comment_id)
                from_user=request.user.username
                if request.user.nickname:
                    from_user=request.user.nickname
                print(new_comment_id)
                print(from_user)
                print(datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M"))
                return HttpResponse(json.dumps({
                    "from_user":from_user,
                    "created_time":datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M"),
                    "content":content,
                    'comment_id':new_comment_id,
                    "errors":""}))
        elif flag=="reply":
            print("flag:--reply")
            comment_id=request.POST.get('commentid',None)
            print("comment_id：",comment_id)
            if comment_id:
                comment=Comment.objects.get(id=comment_id)
                print(comment)
                comment.reply_count=comment.reply_count+1
                comment.save()
                print("coment_count:",comment.reply_count)
                if content:
                    cleaned_data={"from_user":request.user,"content":content,"to_user":comment.from_user}
                    cleaned_data['blog']=blog #不能去掉，联系外键
                    cleaned_data['comment'] = comment #不能去掉，联系外键
                    ReplyComment.objects.create(**cleaned_data)
                    from_user=request.user.username
                    if request.user.nickname:
                        from_user=request.user.nickname
                    to_user=comment.from_user.username
                    if comment.from_user.nickname:
                        to_user=comment.from_user.nickname
                    return HttpResponse(json.dumps({
                        "from_user":from_user,
                        "to_user":to_user,
                        "created_time":datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M"),
                        "content":content,
                        "errors":""}))
    else:
        count.readed=count.readed+1
        form = CommentForm()
    count.save()
    # count.update(blog=blog,readed=readed,commented=commented)
    ctx = {
        'blog': blog,
        'comments': blog.comment_set.all().order_by('-created'),
        'replycomments':blog.replycomment_set.all(),
        'form': form,
        'tags':tags,
        'count':count,
    }
    # 使用render_to_response的话就无法对表单进行验证了，
    # 所以还是需要使用render方法。如果去掉模板中的{% csrf_token %} 用于防跨域请求。就可以了
    return render(request, 'article.html', ctx)

# # 点击了博客列表中的某一项之后跳转到详情界面的方法
# def get_details(request, blog_id):
#     try:
#         blog = Blog.objects.get(id=blog_id)
#         # 获取对应的博客的所有的标签信息
#         tags = blog.tags.all()
#         try:
#             Count.objects.get(blog_id=blog_id)
#         except Count.DoesNotExist:
#             c=Count(blog=blog,readed=0,commented=0)
#             c.save()
#         count=blog.count
#         print(count.commented)
#         readed=0
#         commented=0
#     except Blog.DoesNotExist:
#         raise Http404
#     if request.method == 'GET':
#         form = CommentForm()
#         count.readed=count.readed+1
#     else:
#         form = CommentForm(request.POST)#request.POST提交的数据
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             cleaned_data['blog'] = blog #不能去掉，联系外键
#             # print(cleaned_data)
#             Comment.objects.create(**cleaned_data)
#             count.commented=count.commented+1
#         form =CommentForm()
#     count.save()
#     # count.update(blog=blog,readed=readed,commented=commented)
#     ctx = {
#         'blog': blog,
#         'comments': blog.comment_set.all().order_by('-created'),
#         'form': form,
#         'tags':tags,
#         'count':count,
#     }
#     # 使用render_to_response的话就无法对表单进行验证了，
#     # 所以还是需要使用render方法。如果去掉模板中的{% csrf_token %} 用于防跨域请求。就可以了
#     return render(request, 'blog_details.html', ctx)


# Create your views here.
# def register(request):
#     if request.method == "POST":
#         uf = UserForm(request.POST)
#         if uf.is_valid():
#             #获取表单信息
#             username = uf.cleaned_data['username']
#             password = uf.cleaned_data['passworld']
#             email = uf.cleaned_data['email']
#             #将表单写入数据库
#             smarthome = NormalUser()
#             smarthome.username = username
#             smarthome.password = password
#             smarthome.email = email
#             smarthome.save()
#             #返回注册成功页面
#             return render_to_response('submit_success.html',{'username':username})
#     else:
#         uf = UserForm()
#     return render(request,'register.html',{'uf':uf})

import time

# @csrf_protect
def upload_image(request):
    print("post upload")
    if request.method == 'POST':
        print("come in upload img")
        callback = request.GET.get('CKEditorFuncNum')
        file_name=""
        try:
            path = "upload/" + time.strftime("%Y%m%d%H%M%S",time.localtime())  # <---还有这里，这里path修改你要上传的路径，我记得我是修改了的，这样就上传到了upload文件夹
            f = request.FILES["upload"]
            file_name = path + "_" + f.name
            des_origin_f = open(file_name, "wb+")
            for chunk in f:                 #<--#我修改的是这里，因为python后期的版本放弃了chunk函数，直接遍历类文件类型就可以生成迭代器了。
                des_origin_f.write(chunk)
            des_origin_f.close()
        except Exception, e:
            print e
        res = r"<script>window.parent.CKEDITOR.tools.callFunction("+callback+",'/"+file_name+"', '');</script>"
        return HttpResponse(res)
    else:
        raise Http404()

