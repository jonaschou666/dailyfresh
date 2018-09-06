from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import *
from hashlib import sha1
from . import user_decorator
from df_goods.models import *
from df_order.models import *
from df_cart.models import *
from django.core.paginator import Paginator
def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    #接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    #判断两次密码
    if upwd != ucpwd:
        return redirect('/user/register')
    #密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf8'))
    upwd1 = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd1
    user.uemail = uemail
    user.save()
    #注册成功
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    print(uname)
    count = UserInfo.objects.filter(uname=uname).count()
    print(count)
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)
    #根据用户名查询登录
    users = UserInfo.objects.filter(uname=uname)
    print (uname)
    if len(users)==1:
        s1= sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest()==users[0].upwd:
            url =request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)

    else:
        context = {'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')

@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    #最近浏览
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_ids1=goods_ids.split(',')
    goods_list=[]
    if goods_ids!='':
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context={'title':'用户中心',
             'page_name': 1,
             'goods_list':goods_list,
             'user_email':user_email,
             'user_name':request.session['user_name']}
    return render(request,'df_user/user_center_info.html',context)

#test:
# @user_decorator.login
# def order(request):
#     #test:
#     # uid = request.session.get('user_id')
#     # orderinfos = OrderInfo.objects.filter(o_user_id=uid)
#     # for orderinfo in orderinfos:
#     #     for item in orderinfo.orderdetailinfo_set.all():
#     #         print(item.goods.g_title)
#
#     context={'title':'用户中心','page_name':1,}
#     return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post = request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()
    context={'title':'用户中心','page_name':1,'user':user}
    return render(request,'df_user/user_center_site.html',context)


@user_decorator.login
def order(request,pageid):
    uid = request.session.get('user_id')
    orderinfos = OrderInfo.objects.filter(o_user_id=uid)
    # print(orderinfos)
    # print(pageid)
    # print('========')
    #分页.获取orderinfos list 以两个为一页的list
    paginator = Paginator(orderinfos, 2)
    print(paginator)
    #获取paginator分页后的第pageid的值
    orderlist = paginator.page(int(pageid))
    #取出数据库中的数据数量的集合
    plist = orderinfos.count()
    # print('=========')
    # print(plist)
    # print('=========')
    #dd为当前页
    dd = int(pageid)
    #lenn为取出数据库中的数据的总条数
    lenn = plist
    # print('***********')
    # print(lenn)
    # print('***********')
    if lenn % 2 == 0:
        num_pages = lenn/2
    else:
        num_pages = lenn/2 + 1
    last_page = int(num_pages)
    int_pageid = int(pageid)
    if int_pageid == 1:
        has_previous=False
    else:
        has_previous=True
    if int_pageid == int(num_pages):
        has_next=False
    else:
        has_next=True
    previous_page_number = int_pageid-1
    next_page_number = int_pageid+1

    context={'title':'用户中心','page_name':1,
             'pageid':int(pageid),'orderlist':orderlist,'plist':plist,
             'num_pages':num_pages,'last_page':last_page,
             'previous_page_number':previous_page_number,
             'next_page_number':next_page_number,
             'has_previous':has_previous,'has_next':has_next,
             }
    return render(request,'df_user/user_center_order.html',context)

