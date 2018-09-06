from django.db import models
from tinymce.models import HTMLField
class TypeInfo(models.Model):
    t_title = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.t_title
class GoodsInfo(models.Model):
    g_title = models.CharField(max_length=20)
    g_pic = models.ImageField(upload_to='df_goods')
    g_price = models.DecimalField(max_digits=5,decimal_places=2)
    isDelete = models.BooleanField(default=False)
    g_unit = models.CharField(max_length=20,default='500g')
    g_click = models.IntegerField()
    g_jianjie = models.CharField(max_length=200)
    g_kucun = models.IntegerField()
    g_content = HTMLField()
    g_type = models.ForeignKey(TypeInfo,on_delete=models.CASCADE)
    # g_adv = models.BooleanField(default=False)
    def __str__(self):
        return self.g_title

