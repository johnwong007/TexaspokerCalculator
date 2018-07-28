# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


# Create your models here.
class UserInfo(models.Model):
    nickname = models.CharField(max_length = 50, verbose_name=u'昵称',null=True, blank=True)
    union_id = models.CharField(max_length = 50, verbose_name=u'微信unionid', null=True, blank=True)
    open_id = models.CharField(max_length = 100, verbose_name=u'微信openid', default = '')
    vip_level = models.IntegerField(default=0, verbose_name=u'vip等级')
    add_time = models.DateTimeField(default=datetime.now, verbose_name = u'开始时间')
    desc = models.CharField(max_length = 200, verbose_name=u'备注', null=True, blank=True)
    
    class Meta:
        verbose_name = u'用户信息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        if self.nickname:
            return self.nickname
        return self.open_id
    

class UserChargingOrder(models.Model):
    nickname = models.CharField(max_length = 50, verbose_name=u'昵称',null=True, blank=True)
    union_id = models.CharField(max_length = 50, verbose_name=u'微信unionid', null=True, blank=True)
    open_id = models.CharField(max_length = 100, verbose_name=u'微信openid', default = '')
    order_id = models.CharField(max_length = 30, verbose_name=u'订单id', default = '')    
    charge_num = models.IntegerField(default = 0, verbose_name=u'充值金额')
    order_status = models.IntegerField(default = 0, verbose_name = u'订单状态')#支付状态，0 init 1 成功
    add_time = models.DateTimeField(default=datetime.now, verbose_name = u'添加时间')
    desc = models.CharField(max_length = 500, verbose_name=u'备注', null=True, blank=True)

    class Meta:
        verbose_name = u'用户充值订单表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.add_time)


class UserChargingOrderBak(models.Model):
    '''当请求订单信息不存在时，插入备份表，以供排查'''
    nickname = models.CharField(max_length = 50, verbose_name=u'昵称',null=True, blank=True)
    union_id = models.CharField(max_length = 50, verbose_name=u'微信unionid', null=True, blank=True)
    open_id = models.CharField(max_length = 100, verbose_name=u'微信openid', default = '')
    order_id = models.CharField(max_length = 30, verbose_name=u'订单id', default = '')
    charge_num = models.IntegerField(default = 0, verbose_name=u'充值金额')
    order_status = models.IntegerField(default = 0, verbose_name = u'订单状态')#支付状态，0 init 1 成功
    add_time = models.DateTimeField(default=datetime.now, verbose_name = u'添加时间')
    desc = models.CharField(max_length = 200, verbose_name=u'备注', null=True, blank=True)

    class Meta:
        verbose_name = u'用户充值订单表备份表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.add_time)


