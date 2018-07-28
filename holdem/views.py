#coding:utf8
import sys
import time
import datetime
import json
import traceback
import logging
logging.basicConfig(filename='./jsinfo.log', level=logging.DEBUG)

from django.shortcuts import render
from django.http import HttpResponse

from holdem.models import UserInfo
from holdem.models import UserChargingOrder
from holdem.models import UserChargingOrderBak
from . import HoldemCalculator

# Create your views here.

def test(request):
    return HttpResponse("[\"hello\",\"world\"]")

def calculateEquity(request):
    '''普通德州，普通6+计算接口'''
    try:
        result = 'hello world'
        cards = request.GET.get('cards', None)
        #return HttpResponse(str(cards))
        result = HoldemCalculator.counter(cards)
        return HttpResponse(result)
    except:
        logging.info(traceback.format_exc())
        return HttpResponse("[]")

def calEquityForAll(request):
    '''计算胜率统一接口'''
    try:
        cards = request.GET.get('cards', None)
        tmp = eval(cards)
        calType = tmp.get('type', 1)
        if int(calType) == 0:#短牌花大
            return calEquityForSec6Plus(request)
        elif int(calType) == 2:#短牌葫芦大
            return calculateEquity(request)
        else:#1标准德州
            return calculateEquity(request)

        return HttpResponse("[]")
    except:
        logging.info(traceback.format_exc())
        return HttpResponse("[]")

def calEquityForSec6Plus(request):
    '''花式短牌计算接口'''
    try:
        result = 'hello world'
        cards = request.GET.get('cards', None)
        #return HttpResponse(str(cards))
        result = HoldemCalculator.counterForSpecial6Plus(cards)
        return HttpResponse(result)
    except:
        logging.info(traceback.format_exc())
        return HttpResponse("[]")

def checkUserInfo(request):
    '''status 1有效0无效'''
    try:
        ret = {}
        code = 1
        open_id = request.GET.get('open_id', None)
        if not open_id:
            return HttpResponse(json.dumps({'staus':0, 'desc':'openid can not null'}))
        if open_id=="":
            return HttpResponse(json.dumps({'staus':0, 'desc':'openid is wrong'}))
        user = UserInfo.objects.filter(open_id=open_id)
        if not user:
            user = UserInfo.objects.create()
            user.add_time = datetime.datetime.now()
            user.open_id = str(open_id)
            user.save()
            ret["add_time"] = str(user.add_time)
        else:
            if int(user[0].vip_level)==1:
                code = 2
                ret['desc'] = 'vip'
            else:
                add_time = user[0].add_time
                expire_time = add_time + datetime.timedelta(days=30)
                localtime = datetime.datetime.now()
                if localtime>expire_time:
                    code = 0
                    ret['desc'] = '试用期已过'
                else:
                    deltatime = localtime-add_time
                    ret['desc'] = '在试用期内'
                    ret['days'] = 30-int(deltatime.days)
                ret["add_time"] = str(add_time)
                
        ret["status"] = int(code)
        return HttpResponse(json.dumps(ret))
    except:
        print(traceback.format_exc()) 
        logging.info(traceback.format_exc())
        return HttpResponse(json.dumps({'staus':0, 'desc':'系统异常'}))

def queryChargingOrder(order_id):
    try:
        users = UserChargingOrder.objects.filter(order_id=order_id)
        if users:
            return 1
        else:
            return 0
    except:
        print(traceback.format_exc())
        logging.info(traceback.format_exc())
        return 0

def getChargingOrderInfo(request):
    '''http://47.95.3.79/holdem/getChargingOrderInfo/?order_id=201802013474411'''
    try:
        order_id = request.GET.get("order_id", None)
        if order_id:
            res = queryChargingOrder(order_id)
            ret = {}
            ret['code'] = int(res)
            if int(res)==0:
                ret['desc'] = 'failed'
            else:
                ret['desc'] = 'success'
            return HttpResponse(json.dumps(ret))
        else:
            return HttpResponse("{'code':'0', 'desc':'failed'}")
            
    except:
        print(traceback.format_exc())
        logging.info(traceback.format_exc())
        return HttpResponse("{'code':'0', 'desc':'failed'}")

def createChargingOrder(request):
    ''' 创建订单
    params: 
    data = {
        "union_id":"" #char 微信union_id 可以为空
        "open_id":"" #char 微信open_id 不能为空
        "order_id":"" #char 订单号 不能为空
        "charge_num":0  #int 充值金额 不能为空
        "desc":"" #char 描述信息 可以为空
        "nickname":"" #char wechat name 可以为空
    }

    django会自动为我们创建表holdem_userchargingorder
    '''
    try:
        ret = {}
        status = 0
        data = request.GET.get('data', None)
        if not data:
            return HttpResponse("{'code':'-1'}")
        data = json.loads(data)   
        #print(str(data))
        if type(data) == str or type(data) == unicode:
            data = eval(data)  
        print(type(data))
        if type(data) == dict:
            union_id = data.get("union_id", "")
            open_id = data.get("open_id", None)
            order_id = data.get("order_id", None)
            charge_num = data.get("charge_num", "")
            desc = data.get("desc", "")
            nickname = data.get("nickname", "")
            if not open_id:
                return HttpResponse(json.dumps({'code':'0', 'desc':'open_id can not null'}))
            if not order_id:
                return HttpResponse(json.dumps({'code':'0', 'desc':'order_id can not null'}))
            res = queryChargingOrder(order_id)
            if int(res)==1:
                return HttpResponse(json.dumps({'code':'0', 'desc':'order_id exists'}))
            charging_order = UserChargingOrder.objects.create()
            charging_order.open_id = str(open_id)
            charging_order.order_id = str(order_id)
            charging_order.charge_num = int(charge_num)
            charging_order.union_id = str(union_id)
            charging_order.desc = str(desc)
            charging_order.nickname = nickname
            charging_order.order_status = 0
            charging_order.add_time = datetime.datetime.now()
            charging_order.save()
            userinfo = UserInfo.objects.get(open_id=str(open_id))
            if userinfo:
                userinfo.nickname = nickname
                userinfo.save()
            else:
                userinfo = UserInfo.objects.create()
                userinfo.open_id = str(open_id)
                userinfo.add_time = datetime.datetime.now()
                userinfo.vip_level = 0
                userinfo.nickname = nickname
                userinfo.union_id = ""
                userinfo.desc = ""
                userinfo.save()
            return HttpResponse(json.dumps({'code':'1', 'desc':'success'}))
        return HttpResponse(json.dumps({'code':'0', 'desc':'failed'}))
    except:
        print("创建订单失败")
        print(traceback.format_exc())
        logging.info(traceback.format_exc())

def changeChargingOrderState(request):
    ''' 修改订单状态
    params:
    data = {
        "union_id":"" #char 微信union_id 可以为空
        "open_id":"" #char 微信open_id 可以为空
        "order_id":"" #char 订单号 不能为空
        "charge_num":0  #int 充值金额 可以为空
        "desc":"" #char 描述信息 可以为空
        "nickname":"" #char wechat name 可以为空
    }
    '''
    try:
        data = request.GET.get('data', None)
        if not data:
            return HttpResponse("{'code':'-1'}")

        print(json.dumps(data))
        if type(data) == str or type(data) == unicode:
            data = eval(data)
        #print(type(data))
        if type(data) == dict:
            union_id = data.get("union_id", None)
            open_id = data.get("open_id", None)
            order_id = data.get("order_id", None)
            charge_num = data.get("charge_num", None)
            desc = data.get("desc", None)
            nickname = data.get("nickname", None)
            order_status = data.get("order_status", "1")

            #if not open_id:
            #    return HttpResponse(json.dumps({'code':'0', 'desc':'open_id can not null'}))
            if not order_id:
                return HttpResponse(json.dumps({'code':'0', 'desc':'order_id can not null'}))
            res = queryChargingOrder(order_id)
            if res and int(res) == 1:
                user = UserChargingOrder.objects.get(order_id=order_id)
                if union_id:
                    user.union_id = str(union_id)
                #user.open_id = open_id
                #user.order_id = order_id
                if charge_num:
                    user.charge_num = int(charge_num)
                if desc:
                    user.desc = str(desc)
                if nickname:
                    user.nickname = nickname
                user.order_status = order_status
                user.save()
                print('users.open_id = '+ str(user.open_id))
                print('users.order_id = '+ str(user.order_id))
                print('users.order_status = '+ str(user.order_status))
                
                userinfo = UserInfo.objects.get(open_id=user.open_id)
                if userinfo:
                    userinfo.vip_level = 1
                    userinfo.save()
                return HttpResponse(json.dumps({'code':'1', 'desc':'success'}))
            else:
                if open_id and order_id:
                    print("备份中")
                    charging_order = UserChargingOrderBak.objects.create()
                    charging_order.open_id = str(open_id)
                    charging_order.order_id = str(order_id)
                    charge_num = charge_num or 0
                    charging_order.charge_num = int(charge_num)
                    union_id = union_id or ""
                    charging_order.union_id = str(union_id)
                    desc = desc or ""
                    charging_order.desc = str(desc)
                    nickname = nickname or ""
                    charging_order.nickname = nickname
                    charging_order.order_status = 0
                    charging_order.add_time = datetime.datetime.now()
                    charging_order.save()
                    return HttpResponse(json.dumps({'code':'0', 'desc':'changeChargingOrder failed,saved to bak'}))
 
        return HttpResponse(json.dumps({'code':'0', 'desc':'changeChargingOrder failed'}))
    except:
        print("修改订单失败")
        print(traceback.format_exc())
        logging.info(traceback.format_exc())
        return HttpResponse("{'code':'0', 'desc':'changeChargingOrder failed'}")










