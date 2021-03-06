# coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
import logging
import django.utils.log
import logging.handlers
import json
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
logger = logging.getLogger('sourceDns.webdns.views') 
def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    logger.error('开始进入注册处理。。。。') 
    post=request.POST
    user_name=post.get('user_name')
    pwd=post.get('pwd')
    cpwd=post.get('cpwd')
    email=post.get('email')
    
    #判断密码是否一致，不一致则重定向到注册页
    if pwd!=cpwd:
        #重定向页面
        return redirect('/user/register/')
    #加密处理
    s1=sha1()
    s1.update(pwd)
    upwd3=s1.hexdigest()
    logger.error('加密处理。。。。') 
    #创建对象
    user=UserInfo()
    user.uname=user_name
    user.upwd=pwd
    user.upwd2=upwd3
    user.uemail=email
    user.save()

    #注册成功，转到登录页面a
    return redirect('user/login/')

def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    get=request.POST
    uname=get.get('username')
    upwd=get.get('pwd')
    jizhu=get.get('jizhu',0)

    users=UserInfo.objects.filter(uname=uname)
    print uname

    if len(users)>=1:
        s1=sha1()
        s1.update(upwd)
        gg = s1.hexdigest()+'||'+users[0].upwd2
        logger.error(gg)
        if s1.hexdigest()==users[0].upwd2:
            logger.error('password compare OK...')
            red = HttpResponseRedirect('/user/info/')

            if jizhu != 0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            logger.error('password compare Wrong...')
            contest = {'title':'用户登录','error_name':0, 'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request, 'df_user/login.html')
    else:
            contest = {'title':'用户登录','error_name':1, 'error_pwd':0,'uname':uname,'upwd':upwd}
            return render(request, 'df_user/login.html')








def register_exist(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    logger.error('进行用户存在性检查，用户名[%(uname)s]，返回数量[%(count)s]。。。。')
    print count
    #return JsonResponse({'count':count})
    response_data = {}  
    response_data['count'] = count
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

