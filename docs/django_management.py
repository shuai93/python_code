#!/usr/bin/env python3
# @Time    : 18-1-18 上午11:32
# @Author  : ys
# @Email   : youngs@yeah.net

from .models import User, AppUpdate
from django.db.models.signals import post_migrate
# from django.dispatch import receiver


"""
django migrate 初始化创建数据库，插入数据
完成django初始化的自动插入数据
"""

android = {
    "platform": "android",
    "front": "dlr",
    "version": "2.2.1",
    "url": 'http:isnacai.scsacasa.sacsacsac'
}

ios = {
    "platform": "ios",
    "front": "dlr",
    "version": "1.2.1",
    "url": 'http:isnacai.scsacasa.sacsacsac'
}


# @receiver(post_migrate, sender=User)
# def callback(sender,**kwargs):

# 	user = User.objects.all()
# 	app = AppUpdate.objects.all()
# 	if not all((user,app)):
# 		User.objects.create(name='name', pwd='passwd')
# 		app_list = [AppUpdate(**android),AppUpdate(**ios)]
# 		AppUpdate.objects.bulk_create(app_list)

# 		print('init to create database success')


def callback():
    user = User.objects.all()
    app = AppUpdate.objects.all()
    if not all((user, app)):
        User.objects.create(name='name', pwd='passwd')
        app_list = [AppUpdate(**android), AppUpdate(**ios)]
        AppUpdate.objects.bulk_create(app_list)

        print('init to create database success')


post_migrate.connect(callback, dispatch_uid="my_unique_identifier")
