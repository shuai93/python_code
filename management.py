#!/usr/bin/env python
# @Date    : 2017-06-23 14:34:48
# @Author  : ys (youngs@yeah.net)

from .models import User, AppUpdate
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# django migrate 初始化创建数据库，插入数据

android = {
	"platform":"android",
	"front":"dlr",
	"version":"2.2.1",
	"url":'http:isnacai.scsacasa.sacsacsac'
}
ios = {
	"platform":"ios",
	"front":"dlr",
	"version":"1.2.1",
	"url":'http:isnacai.scsacasa.sacsacsac'
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


def callback(**kwargs):
	user = User.objects.all()
	app = AppUpdate.objects.all()
	if not all((user,app)):
		User.objects.create(name='name', pwd='passwd')
		app_list = [AppUpdate(**android),AppUpdate(**ios)]
		AppUpdate.objects.bulk_create(app_list)

		print('init to create database success')


post_migrate.connect(callback, dispatch_uid="my_unique_identifier")
