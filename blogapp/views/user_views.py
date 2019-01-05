# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from blogapp.models import User
from django.http import HttpResponse
from blogapp import models

from blogapp.blogForms import blogForm

# Create your views here.
#注册功能
def register(request):
    if request.method == 'GET':
        form = blogForm.register()
        return render(request,'blogapp/register.html',{'form':form})
    elif request.method == 'POST':
        form = blogForm.register(request.POST)
        if form.is_valid():
            temp = models.User.objects.filter(userName=form.cleaned_data['userName']).exists()

            if temp == False:
                userModel = User()
                userModel.userName = form.cleaned_data['userName']
                userModel.password = form.cleaned_data['password']

                userModel.save()
                return HttpResponse('数据提交成功!快去登录吧.')
            else:
                error = '用户名已经存在，请换一个用户名试试!'
                return render(request,'blogapp/register.html',{'form':form,'error':error})

        else:
            return render(request,'blogapp/register.html',{'form':form})

#登录功能
def login(request):
    if request.method == 'GET':
        loginform = blogForm.login()
        return render(request,'blogapp/login.html',{'loginform':loginform})
    elif request.method == 'POST':
        loginform = blogForm.login(request.POST,)
        if loginform.is_valid():
            userName = loginform.cleaned_data['userName']
            password = loginform.cleaned_data['password']

            user = models.User.objects.filter(userName=userName).filter(password=password)
            if user.exists():
                request.session['user_id'] = user[0].id

                return render(request,'blogapp/loginsuc.html')
            else:
                error = '用户名或者密码输入有误，请重试'
                return render(request,'blogapp/login.html',{'loginform':loginform,'error':error})
        else:
            return render(request,'blogapp/login.html',{'loginform':loginform})
    else:
        return redirect('https://www.zhihu.com/')

#注销功能
def logout(request):
    userId = request.session.get('user_id',None)
    if not userId == None:
        del request.session['user_id']
        return HttpResponse('注销成功')
    else:
        return HttpResponse('你的操作不合法')

