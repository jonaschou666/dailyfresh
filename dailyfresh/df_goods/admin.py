from django.contrib import admin
from .models import *

class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','t_title']
class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id','g_title','g_price','g_unit',
                    'g_click','g_kucun','g_type']
admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)