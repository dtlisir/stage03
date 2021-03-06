# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-19 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CapacityData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=64, null=True, verbose_name='ip')),
                ('filesystem', models.CharField(max_length=64, verbose_name='filesystem')),
                ('size', models.CharField(max_length=64, verbose_name='size')),
                ('used', models.CharField(max_length=64, verbose_name='used')),
                ('avail', models.CharField(max_length=64, verbose_name='avail')),
                ('use', models.CharField(max_length=64, verbose_name='Use%')),
                ('mounted', models.TextField(max_length=64, verbose_name='mounted')),
                ('createtime', models.DateTimeField(verbose_name='保存时间')),
            ],
            options={
                'verbose_name': '磁盘容量数据',
                'verbose_name_plural': '磁盘容量数据',
            },
        ),
    ]
