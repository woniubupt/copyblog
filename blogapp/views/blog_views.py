# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render,redirect
from blogapp.models import User
from django.http import HttpResponse
from blogapp import models

from blogapp.blogForms import blogForm

from django.core.urlresolvers import reverse #引入重定向的包


#验证用户是否登录
def checkLogin(session):
    #session 键user_id如果不存在对应的值
    id = session.get('user_id',None)
    if id==None:
        #转到登录页面
        return False,redirect(reverse('blogapp:bloglogin'))
    else:
        return True,id

#增加博客内容
def addBlog(request):
    #强制登录验证
    isPassed,next=checkLogin(request.session)
    if not isPassed:
        return next
    if request.method == 'GET':
       blogform = blogForm.BlogForm()
       return render(request,'blogapp/addblog.html',{'blogform':blogform})
    elif request.method == 'POST':
        submitForm = blogForm.BlogForm(request.POST,request.FILES)
        if submitForm.is_valid():
            newBlog = models.Blog()
            newBlog.pic = submitForm.cleaned_data['pic']
            newBlog.title = submitForm.cleaned_data['title']
            newBlog.content = submitForm.cleaned_data['content']
            newBlog.authorId = request.session['user_id']

            newBlog.save()

            return HttpResponse('发表成功QAQ.')
        else:
            return render(request,'blogapp/addblog.html',{'blogform':submitForm})

#显示首页
def index(request):
    return render(request,'blogapp/index.html')



#显示博客列表
def list(request):
    isPassed,next=checkLogin(request.session)
    if not isPassed:
        return next
    userId = request.session.get('user_id')
    #查找authorId和session中和user_id一致的博客
    list = models.Blog.objects.filter(authorId=userId).filter(isDelete=1)
    return render(request,'blogapp/bloglist.html',{'blogs':list})

#显示博客文章内容
def detailBlog(request):
    isPassed,next=checkLogin(request.session)
    if not isPassed:
        return next
    #从选择器中提取博客ID
    blogId = request.GET.get('blogid',0) #默认为0
    blog = models.Blog.objects.get(pk=blogId)
    return render(request,'blogapp/detailblog.html',{'blog':blog})

#修改博客内容
def editBlog(request):
    isPassed,next=checkLogin(request.session)
    if not isPassed:
        return next
    if request.method == 'GET':
        #从选择器中提取博客ID
        blogId = request.GET.get('blogid',0)
        blog = models.Blog.objects.get(pk=blogId)
        blogform = blogForm.BlogForm(initial={
                'title':blog.title,
                'content':blog.content,
                'pic':blog.pic
        })
        return render(request,'blogapp/editblog.html',{'blogform':blogform,'id':blogId})
    elif request.method == 'POST':
        submitForm = blogForm.BlogForm(request.POST,request.FILES)
        id = request.POST.get('id',0)
        if submitForm.is_valid():
            user_id = request.session['user_id']
            #查找当前用户发表的博客
            newBlog = models.Blog.objects.filter(authorId=user_id)[0]
            newBlog.pic = submitForm.cleaned_data['pic']
            newBlog.title = submitForm.cleaned_data['title']
            newBlog.content = submitForm.cleaned_data['content']

            newBlog.save()
            return redirect(reverse('blogapp:bloglist')) #重定向到博客首页

        else:
            return render(request,'blogapp/editblog.html',{'blogform':submitForm,'id':id})

#删除博客内容
def delBlog(request):
    isPassed,next=checkLogin(request.session)
    if not isPassed:
        return next
    if request.method == 'GET':
        blogId = request.GET.get('blogid',0)
        blog = models.Blog.objects.get(pk=blogId)
        if blog.authorId == request.session['user_id']:
            blog.isDelete=0
            blog.save()
            blog = models.Blog.objects.all().filter(isDelete=1)
            return redirect(reverse('blogapp:bloglist')) #重定向到博客首页
        else:
            return HttpResponse('抱歉，您无权进行此操作！！！')


#查找博客内容
def search(request):
    isPassed,next=checkLogin(request.session)
    if not isPassed:
        return next
    userId = request.session.get('user_id')
    #得到关键词
    keyword = request.GET.get('keyword',None)
    # 查找authorId和session中和user_id一致的博客
    list = models.Blog.objects.filter(authorId=userId).filter(isDelete=1).filter(title__contains=keyword)
    #注意这里的title__contains是双划线
    return render(request, 'blogapp/bloglist.html', {'blogs': list})

