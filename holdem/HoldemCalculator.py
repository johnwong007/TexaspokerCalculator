#coding:utf8
import os
import sys
import time
import datetime
import traceback
import GetWinInfo
import commands

import requests
from requests import Request,Session

import urllib
import urllib2
from urllib import urlencode

import json

import logging
logging.basicConfig(filename='./jsinfo.log', level=logging.DEBUG)

cards_transfer={
'12':'ac','38':'ad','25':'ah','51':'as',#A
'11':'kc','37':'kd','24':'kh','50':'ks',#K
'10':'qc','36':'qd','23':'qh','49':'qs',#Q
'9':'jc','35':'jd','22':'jh','48':'js',#J
'8':'tc','34':'td','21':'th','47':'ts',#10
'7':'9c','33':'9d','20':'9h','46':'9s',#9
'6':'8c','32':'8d','19':'8h','45':'8s',#8
'5':'7c','31':'7d','18':'7h','44':'7s',#7
'4':'6c','30':'6d','17':'6h','43':'6s',#6
'3':'5c','29':'5d','16':'5h','42':'5s',#5
'2':'4c','28':'4d','15':'4h','41':'4s',#4
'1':'3c','27':'3d','14':'3h','40':'3s',#3
'0':'2c','26':'2d','13':'2h','39':'2s',#2
}

reverse_cards_transfer={
'ac':'12','ad':'38','ah':'25','as':'51',#A
'kc':'11','kd':'37','kh':'24','ks':'50',#K
'qc':'10','qd':'36','qh':'23','qs':'49',#Q
'jc':'9','jd':'35','jh':'22','js':'48',#J
'tc':'8','td':'34','th':'21','ts':'47',#10
'9c':'7','9d':'33','9h':'20','9s':'46',#9
'8c':'6','8d':'32','8h':'19','8s':'45',#8
'7c':'5','7d':'31','7h':'18','7s':'44',#7
'6c':'4','6d':'30','6h':'17','6s':'43',#6
'5c':'3','5d':'29','5h':'16','5s':'42',#5
'4c':'2','4d':'28','4h':'15','4s':'41',#4
'3c':'1','3d':'27','3h':'14','3s':'40',#3
'2c':'0','2d':'26','2h':'13','2s':'39',#2
'Ac':'12','Ad':'38','Ah':'25','As':'51',#A
'Kc':'11','Kd':'37','Kh':'24','Ks':'50',#K
'Qc':'10','Qd':'36','Qh':'23','Qs':'49',#Q
'Jc':'9','Jd':'35','Jh':'22','Js':'48',#J
'Tc':'8','Td':'34','Th':'21','Ts':'47',#10
}

cardFilterList6_1 = [
'3','29','16','42',#5
'2','28','15','41',#4
'1','27','14','40',#3
'0','26','13','39'#2
]

def counter(cards):
        '''微信小程序'''
        try:
            #cards = "{'200B':['6','9','16'],'dead':['2'],'2001':[{'isPreflop':'1','200F':'1','201C':['AKs']},{'isPreflop':'0','200F':'4','201C':['8','9']}]}"
            print(cards)
            cards = eval(cards)
            community = cards['200B']
            dead = cards['dead']
            user_hands = cards['2001']
            card_type = cards.get('type', 0)
            if int(card_type)==0 or int(card_type)==2:
                for card in cardFilterList6_1:
                    dead.append(card)
            evalInput = './ps-eval'
            
            preflopNum = 0
            for user in user_hands:
                isPreflop = user['isPreflop']
                if int(isPreflop) == 1:
                    preflopNum = preflopNum+1

            for user in user_hands:
                isPreflop = user['isPreflop']
                if int(isPreflop) == 0:
                    hand1 = user['201C'][0]
                    hand2 = user['201C'][1]
                    hand1 = cards_transfer[str(hand1)]
                    hand2 = cards_transfer[str(hand2)]
                    evalInput = evalInput+' '+str(hand1)+str(hand2)
                else:
                    evalInput = evalInput+' '
               
                    #for i in range(len(user['201C'])):
                    #    if i!=0:
                    #        evalInput = evalInput+','+GetWinInfo.getAllCardFromPreflop(user['201C'][i])
                    #    else:
                    #        evalInput = evalInput+GetWinInfo.getAllCardFromPreflop(user['201C'][i])

                    result = GetWinInfo.getAverageEquityFromPreflop(user['201C'])
                    if preflopNum>3:
                        #evalInput = evalInput+str(GetWinInfo.cards2str(GetWinInfo.getCardsFromSinglePreflop(result)))    
                        evalInput = evalInput+str(GetWinInfo.randomTwoHandCard(GetWinInfo.getCardsFromSinglePreflop(result)))    
                    else:
                        #evalInput = evalInput+str(GetWinInfo.cards2str(GetWinInfo.getCardsFromSinglePreflop(result)))    
                        evalInput = evalInput+str(GetWinInfo.randomTwoHandCard(GetWinInfo.getCardsFromSinglePreflop(result)))    
            print('evalInput:'+evalInput)  
                
            if type(community)==list and len(community)>0:
                evalInput = evalInput + ' --board '
            for card in community:
                evalInput = evalInput + str(cards_transfer[str(card)])
            if type(dead)==list and len(dead)>0:
                evalInput = evalInput + ' --dead  '
            for card in dead:
                evalInput = evalInput + str(cards_transfer[str(card)])
            print('evalInput:'+evalInput)            
            #result = commands.getoutput('./ps-eval AcAs Kh4d --board 5c8s9h --dead tctdthts')
            result = commands.getoutput(evalInput)
            print(result)
            #data = eval(result)
            return result 
        except:
            print(traceback.format_exc())
            return "system error!"

'''
url : https://miniapp.pokermate.cn/doCalc?data= 
data : {"Mode":2,"CommunityCards":[],"Players":[{"Id":0,"HoleCards":[12,38]},{"Id":1,"HoleCards":[8,34]}]})
response :

{
code: "0",
data: "{"Players_rate":[{"Id":0,"Win":69.751,"Tie":0.997,"NLose":70.2},{"Id":1,"Win":29.252,"Tie":0.997,"NLose":29.8}]}",
message: "请求成功",
timestamp: "31017-10-3131 17:51:50"
}
'''

def counterForSpecial6Plus(cards):
        '''花式短牌计算器'''
        try:
            #logging.info('counterForSpecial6Plus')
            #cards = '{"200B":["6","9","16"],"dead":["2"],"2001":[{"isPreflop":"1","200F":"1","201C":["AKs"]},{"isPreflop":"0","200F":"0","201C":["8","7"]}]}'
            print(cards)
            cards = eval(cards)
            community = cards["200B"]
            dead = cards["dead"]
            user_hands = cards["2001"]
            card_type = cards.get("type", 0)
            if int(card_type)==0:
                for card in cardFilterList6_1:
                    dead.append(card)
            evalInput = "./ps-eval"

            used_cards = []
            # 拼装数据
            data2pokermate = {}
            data2pokermate["Mode"] = 2
            data2pokermate["CommunityCards"] = community
            for i in range(len(data2pokermate["CommunityCards"])):
                data2pokermate["CommunityCards"][i] = int(data2pokermate["CommunityCards"][i])
            data2pokermate["Players"] = []
            for i in range(len(user_hands)):
                user2p = {}
                user2p["isPreflop"] = user_hands[i]["isPreflop"]
                user2p["Id"] = int(user_hands[i]["200F"])
                user2p["HoleCards"] = user_hands[i]["201C"]
                if int(user2p["isPreflop"])==0:
                    for j in range(len(user2p["HoleCards"])):
                        user2p["HoleCards"][j] = int(user2p["HoleCards"][j])
                        used_cards.append(user2p["HoleCards"][j])
                data2pokermate["Players"].append(user2p)
            #print(used_cards)

            for i in range(len(data2pokermate["Players"])):
                if int(data2pokermate["Players"][i]["isPreflop"])==1:
                    #print('yes')
                    data2pokermate["Players"][i]["HoleCards"] = GetWinInfo.getDiffHandCard(data2pokermate["Players"][i]["HoleCards"], used_cards)
                del data2pokermate["Players"][i]["isPreflop"]
            print(str(data2pokermate))    

            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
            url = 'https://miniapp.pokermate.cn/doCalc?data='
            #'{"Players":%20[{"HoleCards":%20[25,%2024],%20"Id":%201},%20{"HoleCards":%20[8,%207],%20"Id":%200}],%20"CommunityCards":%20[6,%209,%2016],%20"Mode":%202}'
            tmpData = str(data2pokermate)
            tmpData = tmpData.replace('\"', '%22')
            tmpData = tmpData.replace('\'', '%22')
            tmpData = tmpData.replace(' ', '%20')
            url = url+tmpData
            print(url)
            req = urllib2.Request(url, headers=headers)
            result = urllib2.urlopen(req).read()
            startpos = result.find('{') 
            endpos = result.rfind('}') 
            result = result[startpos:endpos+1]
            print(str(type(result)))       
            finalResult = []
            if result and type(result) == str:
                result = eval(result)
            if result and type(result) == dict:
                print('1111')
                if int(result['code'])==0:
                    print('2222')
                    if result['data'] and type(result['data'])==str:
                        print('3333')
                        result_data = eval(result['data'])
                        print(result_data)
                        print(type(result_data))

                        for i in range(len(result_data['Players_rate'])):
                            for j in range(i+1, len(result_data['Players_rate'])):
                                if int(result_data['Players_rate'][i]['Id'])>int(result_data['Players_rate'][j]['Id']):
                                    tmp = result_data['Players_rate'][i]
                                    result_data['Players_rate'][i] = result_data['Players_rate'][j]
                                    result_data['Players_rate'][j] = tmp

                        for i in range(len(result_data['Players_rate'])):
                            tmpResult = []
                            nlose = round(float(result_data['Players_rate'][i]['NLose']), 2)
                            tmpResult.append(nlose)
                            win = round(float(result_data['Players_rate'][i]['Win']), 2)
                            tmpResult.append(win)
                            tie = round(float(result_data['Players_rate'][i]['Tie']), 2)
                            tmpResult.append(tie)
                            #tmpResult.append(result_data['Players_rate'][i]['Id'])
                            #tmpResult.append(result_data['Players_rate'][i]['NLose'])
                            #tmpResult.append(result_data['Players_rate'][i]['Win'])
                            #tmpResult.append(result_data['Players_rate'][i]['Tie'])
                            finalResult.append(tmpResult)            

            return str(finalResult)

        except:
            logging.info(traceback.format_exc())
            return "system error!"

if __name__ == '__main__':
        result = counterForSpecial6Plus(None)
        print(result)
        #logging.info(str(result))


