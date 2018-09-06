#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from df_user import user_decorator
from df_user.models import UserInfo
from df_cart.models import *
from df_goods.models import *
from django.db import transaction
from .models import *
from datetime import datetime
from decimal import Decimal

@user_decorator.login
def order(request):
    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)

    #获取勾选的每一个订单对象，构造成list，作为上下文传入下单页面
    orderid = request.GET.getlist('orderid')
    print('===========')
    print(orderid)
    print('===========')
    orderlist = []

    for id in orderid:
        orderlist.append(CarInfo.objects.get(goods_id=int(id)))

    if user.uphone == '':
        uphone =''
    else:
        uphone = user.uphone[0:4]+'****'+user.uphone[-4:]

    context = {'title':'提交订单','page_name':1,
               'orderlist':orderlist,'user':user,
               'ureceiver_phone':uphone}

    return render(request,'df_order/place_order.html',context)

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    #保存一个事务点
    tran_id=transaction.savepoint()
    #接收购物车编号
    #根据ＰＯＳＴ和ｓｅｓｓｉｏｎ获取信息
    try:
        post = request.POST
        orderlist = post.getlist('id[]')
        print(orderlist)
        total = post.get('total')
        address = post.get('address')

        order = OrderInfo()
        now = datetime.now()
        uid = request.session.get('user_id')

        order.o_id = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.o_user_id = uid
        order.o_date = now
        order.o_total = Decimal(total)
        order.o_address = address
        order.save()

        #遍历购物车中提交的信息，创建订单详情表
        for orderid in orderlist:
            print(orderid)
            cartinfo = CarInfo.objects.get(goods_id=orderid)

            good = GoodsInfo.objects.get(id=cartinfo.goods_id)

            if int(good.g_kucun) >= int(cartinfo.count):
                good.g_kucun -= int(cartinfo.count)
                good.save()
                #创建订单详情表
                detialinfo = OrderDetailInfo()
                detialinfo.goods_id = int(good.id)
                detialinfo.order_id = int(order.o_id)
                detialinfo.price = Decimal(good.g_price)
                detialinfo.count = int(cartinfo.count)
                detialinfo.save()

                cartinfo.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'status':2})
    except Exception as e:
        print('====================%s'%e)
        transaction.savepoint_rollback(tran_id)

    return JsonResponse({'status':1})
# def pay(request):
#     pass
@user_decorator.login
def delete(request,order_id):
    try:
        order=OrderInfo.objects.get(pk=int(order_id))
        order.delete()
        data={'ok':1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)