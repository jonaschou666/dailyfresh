from django.db import models

class OrderInfo(models.Model):
    o_id=models.CharField(max_length=20,primary_key=True)
    o_user=models.ForeignKey("df_user.UserInfo",on_delete=models.CASCADE)
    o_date=models.DateTimeField(auto_now=True)
    o_IsPay=models.BooleanField(default=False)
    o_total=models.DecimalField(max_digits=6,decimal_places=2)
    o_address=models.CharField(max_length=150,default='')

class OrderDetailInfo(models.Model):
    goods=models.ForeignKey('df_goods.GoodsInfo',on_delete=models.CASCADE)
    order=models.ForeignKey(OrderInfo,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    count=models.IntegerField()

