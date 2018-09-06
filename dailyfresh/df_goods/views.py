#coding=utf-8
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator,Page
from df_cart.models import *


def index(request):
    typelist = TypeInfo.objects.all()
    cart_count = CarInfo.objects.all().count()
    type0=typelist[0].goodsinfo_set.order_by('-id')[0:3]
    type01=typelist[0].goodsinfo_set.order_by('-g_click')[0:3]
    type1=typelist[1].goodsinfo_set.order_by('-id')[0:3]
    type11=typelist[1].goodsinfo_set.order_by('-g_click')[0:3]
    type2=typelist[2].goodsinfo_set.order_by('-id')[0:3]
    type21=typelist[2].goodsinfo_set.order_by('-g_click')[0:3]
    type3=typelist[3].goodsinfo_set.order_by('-id')[0:3]
    type31=typelist[3].goodsinfo_set.order_by('-g_click')[0:3]
    type4=typelist[4].goodsinfo_set.order_by('-id')[0:3]
    type41=typelist[4].goodsinfo_set.order_by('-g_click')[0:3]
    type5=typelist[5].goodsinfo_set.order_by('-id')[0:3]
    type51=typelist[5].goodsinfo_set.order_by('-g_click')[0:3]
    context = {'title':'首页','guest_cart':1,'cart_count':cart_count,
               'type0':type0,'type01':type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,}
    return render(request,'df_goods/index.html',context)

def list(request,tid,pindex,sort):
    cart_count = CarInfo.objects.all().count()
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':
        goods_list=GoodsInfo.objects.filter(g_type_id=int(tid)).order_by('-id')
    elif sort == '2':
        goods_list=GoodsInfo.objects.filter(g_type_id=int(tid)).order_by('-g_price')
    elif sort == '3':
        goods_list=GoodsInfo.objects.filter(g_type_id=int(tid)).order_by('-g_click')
    paginator = Paginator(goods_list,10)
    page=paginator.page(int(pindex))
    context={'title':typeinfo.t_title,'guest_cart':1,'cart_count':cart_count,
             'page':page,'paginator':typeinfo,
        'typeinfo':typeinfo,'sort':sort,'news':news}
    return render(request,'df_goods/list.html',context)

def detail(request,id):
    cart_count = CarInfo.objects.all().count()
    print('hahahahhhahahah')
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.g_click=goods.g_click+1
    goods.save()
    news=goods.g_type.goodsinfo_set.order_by('-id')[0:2]
    context = {'title':goods.g_type.t_title,'guest_cart':1,'cart_count':cart_count,
               'g':goods,'news':news,'id':id}
    response = render(request,'df_goods/detail.html',context)

    #记录最近浏览，在用户中心使用
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_id = '%d'%goods.id
    if goods_ids!='': #判断是否有游览记录，如果有则继续判断
        goods_ids1=goods_ids.split(',')#拆分为列表
        if goods_ids1.count(goods_id)>=1:#如果商品已经被记录，则删除
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)#添加到第一个　
        if len(goods_ids1)>=6:#如果超过６个则删除最后一个
            del goods_ids1[5]
        goods_ids=','.join(goods_ids1)#拼接为字符串
    else:
        goods_ids=goods_id#如没有浏览记录则直接加
    response.set_cookie('goods_ids',goods_ids)#写入ｃｏｏｋｉｅ

    return response