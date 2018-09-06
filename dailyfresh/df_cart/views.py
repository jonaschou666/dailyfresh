from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from df_user import user_decorator
from .models import *

@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CarInfo.objects.filter(user_id=uid)
    context={'title':'购物车',
             'page_name':1,
             'carts':carts}
    return render(request,'df_cart/cart.html',context)

@user_decorator.login
def add(request,gid,count):
    #用户ｕｉｄ购买类ｇｉｄ商品，数量为ｃｏｕｎｔ
    uid = request.session['user_id']
    gid = int(gid)
    #查询购物车中是否已经有此商品，如果有，则数量增加，如果没有则新增
    carts=CarInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts)>=1:
        cart = carts[0]
        cart.count = cart.count+int(count)
    else:
        cart=CarInfo()
        cart.user_id=uid
        cart.goods_id=gid
        cart.count = count
    cart.save()
    #如果是ａｊａｘ请求则返回ｊｓｏｎ，否则转向购物车
    if request.is_ajax():
        count=CarInfo.objects.filter(user_id=request.session['user_id'])
        return JsonResponse({'count':count})
    else:
        return HttpResponseRedirect('/cart/')

@user_decorator.login
def edit(request,cart_id,count):
    try:
        cart=CarInfo.objects.get(pk=int(cart_id))
        count1=cart.count=int(count)
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok':count1}
    return JsonResponse(data)

@user_decorator.login
def delete(request,cart_id):
    try:
        cart=CarInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data={'ok':1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)



