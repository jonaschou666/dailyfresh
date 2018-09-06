# Generated by Django 2.1 on 2018-08-21 15:26

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_title', models.CharField(max_length=20)),
                ('g_pic', models.ImageField(upload_to='df_goods')),
                ('g_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('isDelete', models.BooleanField(default=False)),
                ('g_unit', models.CharField(default='500g', max_length=20)),
                ('g_click', models.IntegerField()),
                ('g_jianjie', models.CharField(max_length=200)),
                ('g_kucun', models.IntegerField()),
                ('g_content', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_title', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='g_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='df_goods.TypeInfo'),
        ),
    ]
