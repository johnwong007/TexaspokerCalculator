# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from holdem.models import UserInfo,UserChargingOrder,UserChargingOrderBak

# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("nickname","open_id", "vip_level", "add_time", "desc")
    search_fields = ("nickname","open_id", "vip_level", "add_time", "desc")
    list_filter = ("nickname","open_id", "vip_level", "add_time", "desc")
    ordering = ("-add_time",)

class UserChargingOrderAdmin(admin.ModelAdmin):
    list_display = ("nickname","open_id", "order_id", "order_status", "add_time", "desc")
    search_fields = ("nickname","open_id", "order_id", "order_status", "add_time", "desc")
    list_filter = ("nickname","open_id", "order_id", "order_status", "add_time", "desc")
    ordering = ("-add_time",)

class UserChargingOrderBakAdmin(admin.ModelAdmin):
    list_display = ("nickname","open_id", "order_id", "order_status", "add_time", "desc")
    search_fields = ("nickname","open_id", "order_id", "order_status", "add_time", "desc")
    list_filter = ("nickname","open_id", "order_id", "order_status", "add_time", "desc")
    ordering = ("-add_time",)

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserChargingOrder, UserChargingOrderAdmin)
admin.site.register(UserChargingOrderBak, UserChargingOrderBakAdmin)

admin.site.site_header = u"广阔天空德州扑克计算器微信小程序"



