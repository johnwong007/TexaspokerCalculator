#coding:utf8
import time
import random
import copy
import thread
import sys
# import zlog as logging
import copy

cardPoint = {'11':'J', '12':'Q', '13':'K', '1':'A'} 
cardFilterList6_1 = ['0_2', '1_2', '2_2', '3_2', '0_3', '1_3', '2_3', '3_3', '0_4', '1_4', '2_4', '3_4', '0_5', '1_5', '2_5', '3_5']
cardFilterTest = ['0_A', '0_6', '0_7', '0_8', '0_9']
cardlist = []
thread_num = 1
run_num = 1
# run_num = 1310

cards_transfer={
'0':'ac','38':'ad','25':'ah','51':'as',#A
'1':'kc','37':'kd','24':'kh','50':'ks',#K
'2':'qc','36':'qd','23':'qh','49':'qs',#Q
'3':'jc','35':'jd','22':'jh','48':'js',#J
'4':'tc','34':'td','21':'th','47':'ts',#10
'5':'9c','33':'9d','20':'9h','46':'9s',#9
'6':'8c','32':'8d','19':'8h','45':'8s',#8
'7':'7c','31':'7d','18':'7h','44':'7s',#7
'8':'6c','30':'6d','17':'6h','43':'6s',#6
'9':'5c','29':'5d','16':'5h','42':'5s',#5
'10':'4c','28':'4d','15':'4h','41':'4s',#4
'11':'3c','27':'3d','14':'3h','40':'3s',#3
'12':'2c','26':'2d','13':'2h','39':'2s',#2
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

card_color = {
    '0':'c','1':'d','2':'h','3':'s',
}
pfPocketEquity = {
    'AA':   0.852037,
    'AKs':  0.670446,
    'AQs':  0.662089,
    'AJs':  0.653927,
    'ATs':  0.646024,
    'A9s':  0.627812,
    'A8s':  0.619438,
    'A7s':  0.60984,
    'A6s':  0.599058,
    'A5s':  0.599229,
    'A4s':  0.590336,
    'A3s':  0.582203,
    'A2s':  0.573789,
    'AKo':  0.653201,
    'KK':   0.823957,
    'KQs':  0.634004,
    'KJs':  0.625673,
    'KTs':  0.617886,
    'K9s':  0.599885,
    'K8s':  0.583123,
    'K7s':  0.575377,
    'K6s':  0.566407,
    'K5s':  0.557929,
    'K4s':  0.548846,
    'K3s':  0.54055,
    'K2s':  0.532117,
    'AQo':  0.644318,
    'KQo':  0.614558,
    'QQ':   0.799252,
    'QJs':  0.602592,
    'QTs':  0.594676,
    'Q9s':  0.576643,
    'Q8s':  0.560177,
    'Q7s':  0.543023,
    'Q6s':  0.536126,
    'Q5s':  0.527694,
    'Q4s':  0.518553,
    'Q3s':  0.510192,
    'Q2s':  0.50169,
    'AJo':  0.635633,
    'KJo':  0.605687,
    'QJo':  0.581347,
    'JJ':   0.774695,
    'JTs':  0.575279,
    'J9s':  0.556625,
    'J8s':  0.540156,
    'J7s':  0.523248,
    'J6s':  0.506059,
    'J5s':  0.499868,
    'J4s':  0.490705,
    'J3s':  0.482316,
    'J2s':  0.473782,
    'ATo':  0.627217,
    'KTo':  0.597389,
    'QTo':  0.572908,
    'JTo':  0.552477,
    'TT':   0.750118,
    'T9s':  0.540275,
    'T8s':  0.523344,
    'T7s':  0.50639,
    'T6s':  0.489407,
    'T5s':  0.472163,
    'T4s':  0.465305,
    'T3s':  0.456925,
    'T2s':  0.448395,
    'A9o':  0.607728,
    'K9o':  0.578119,
    'Q9o':  0.553604,
    'J9o':  0.532512,
    'T9o':  0.515317,
    '99':   0.720573,
    '98s':  0.508008,
    '97s':  0.491177,
    '96s':  0.474283,
    '95s':  0.457219,
    '94s':  0.43862,
    '93s':  0.432643,
    '92s':  0.424152,
    'A8o':  0.598726,
    'K8o':  0.560202,
    'Q8o':  0.535998,
    'J8o':  0.514902,
    'T8o':  0.497213,
    '98o':  0.48097,
    '88':   0.69163,
    '87s':  0.479363,
    '86s':  0.462433,
    '85s':  0.44545,
    '84s':  0.427016,
    '83s':  0.408735,
    '82s':  0.402716,
    'A7o':  0.588412,
    'K7o':  0.551874,
    'Q7o':  0.517657,
    'J7o':  0.496819,
    'T7o':  0.479081,
    '97o':  0.462978,
    '87o':  0.450508,
    '77':   0.66236,
    '76s':  0.453718,
    '75s':  0.436755,
    '74s':  0.418493,
    '73s':  0.400359,
    '72s':  0.381559,
    'A6o':  0.576825,
    'K6o':  0.542233,
    'Q6o':  0.510241,
    'J6o':  0.478443,
    'T6o':  0.46092,
    '96o':  0.444913,
    '86o':  0.432409,
    '76o':  0.423227,
    '66':   0.632847,
    '65s':  0.431334,
    '64s':  0.413333,
    '63s':  0.395336,
    '62s':  0.37669,
    'A5o':  0.576965,
    'K5o':  0.53314,
    'Q5o':  0.501201,
    'J5o':  0.471809,
    'T5o':  0.442509,
    '95o':  0.426691,
    '85o':  0.414275,
    '75o':  0.40512,
    '65o':  0.399443,
    '55':   0.603249,
    '54s':  0.414534,
    '53s':  0.39693,
    '52s':  0.378493,
    'A4o':  0.567297,
    'K4o':  0.523275,
    'Q4o':  0.491277,
    'J4o':  0.461864,
    'T4o':  0.435041,
    '94o':  0.406711,
    '84o':  0.394468,
    '74o':  0.385498,
    '64o':  0.380105,
    '54o':  0.381553,
    '44':   0.570228,
    '43s':  0.386419,
    '42s':  0.36829,
    'A3o':  0.558446,
    'K3o':  0.514257,
    'Q3o':  0.482194,
    'J3o':  0.452755,
    'T3o':  0.425946,
    '93o':  0.400195,
    '83o':  0.374838,
    '73o':  0.366023,
    '63o':  0.360776,
    '53o':  0.362648,
    '43o':  0.351459,
    '33':   0.536931,
    '32s':  0.359844,
    'A2o':  0.549286,
    'K2o':  0.505087,
    'Q2o':  0.472954,
    'J2o':  0.443485,
    'T2o':  0.416684,
    '92o':  0.390979,
    '82o':  0.368277,
    '72o':  0.345836,
    '62o':  0.340751,
    '52o':  0.342846,
    '42o':  0.331998,
    '32o':  0.323032,
    '22':   0.50334
}


def initCardList():
    del cardlist[:]
    for i in range( 1, 14 ):
        for j in range( 4 ):
            if i > 10 or i == 1:
                cardlist.append( str(j) + '_' + cardPoint[ str( i ) ] )
            else:
                cardlist.append( str(j) + '_' + str ( i ) )

def shuffle():
    random.seed( time.time() )
    cyc_num = ( int( 10 * random.random() )%3 )+1
    for i in range( cyc_num ):
        random.shuffle(cardlist)

def getOneCard(tableSubType = 0, filterFlag = 0):
    single_card = cardlist.pop( 0 )
    cardlist.append( single_card )
    return single_card

def setValue(aa):
    cc = []
    for i in aa:
        if i not in cc:
            cc.append(i)
    return cc

def toClass(array):#拆分花色和值
    color = []
    value = []
    for i in array:
        color.append(i['color'])
        value.append(i['value'])
    return color,value

def toClassByIndex(array, indexList):#拆分花色和值
    color = []
    value = []
    for i in range(len(indexList)):
        if indexList[i] == 1:
            color.append(array[i]['color'])
            value.append(array[i]['value'])
    return color,value

def isRoyalFlush(array):#ROYAL_FLUSH
    royalFlush = ['A','K','Q','J','10']
    color,value = toClass(array)
    value.sort()
    royalFlush.sort()
    if isFlush(array) == 1: #判断是否为FLUSH
        if royalFlush == value: #判断是否为['A','K','Q','J','10']
            return 1
        else :
            return 0
    else :
        return 0

def isRoyalFlushByIndex(array, indexList):#ROYAL_FLUSH
    royalFlush = ['A','K','Q','J','10']
    color,value = toClassByIndex(array, indexList)
    value.sort()
    royalFlush.sort()
    if isFlush(array) == 1: #判断是否为FLUSH
        if royalFlush == value: #判断是否为['A','K','Q','J','10']
            return 1
        else :
            return 0
    else :
        return 0

def isStraightFlush(array, subTableType):#STRAIGHT_FLUSH
    if isFlush(array) == 1:
        if isStraight(array, subTableType) == 1:
            return 1
        else:
            return 0
    else:
        return 0

def isStraightFlushByIndex(array, subTableType, listIndex):#STRAIGHT_FLUSH
    if isFlush(array, listIndex) == 1:
        if isStraight(array, subTableType, listIndex) == 1:
            return 1
        else:
            return 0
    else:
        return 0
    
def isFourOfKind(array):#FOUR_OF_A_KIND
    color,value = toClass(array)
    if len(setValue(value)) == 2 :
        if value.count(value[0]) in (1,4):
            return 1
        else:
            return 0
    else:
        return 0
    
def isFourOfKindByIndex(array, listIndex):#FOUR_OF_A_KIND
    color,value = toClassByIndex(array, indexList)
    if len(setValue(value)) == 2 :
        if value.count(value[0]) in (1,4):
            return 1
        else:
            return 0
    else:
        return 0

def isFullHouse(array):#BOAT_OR_FULL_HOUSE
    color,value = toClass(array)
    if len(setValue(value)) == 2 :
        if value.count(value[0]) in (2,3):
            return 1
        else:
            return 0
    else:
        return 0

def isFullHouseByIndex(array, indexList):#BOAT_OR_FULL_HOUSE
    color,value = toClassByIndex(array, indexList)
    if len(setValue(value)) == 2 :
        if value.count(value[0]) in (2,3):
            return 1
        else:
            return 0
    else:
        return 0
  

def isFlush(array):#FLUSH
    color,value = toClass(array)
    if color.count(color[0]) == len(color): #判断是否为FLUSH
        return 1
    else:
        return 0
  

def isFlushByIndex(array, indexList):#FLUSH
    color,value = toClassByIndex(array, indexList)
    if color.count(color[0]) == len(color): #判断是否为FLUSH
        return 1
    else:
        return 0
    

def isStraight(array, subTableType):#STAIGHT
    # subTableType = 2
    if (int(subTableType) == 1 or int(subTableType) == 2 ):
        straightDir = [['A','K','Q','J','10'],['K','Q','J','10','9'],['Q','J','10','9','8'],
                       ['J','10','9','8','7'],['10','9','8','7','6'],['9','8','7','6','A']]
    else:
        straightDir = [['A','K','Q','J','10'],['K','Q','J','10','9'],['Q','J','10','9','8'],
                       ['J','10','9','8','7'],['10','9','8','7','6'],['9','8','7','6','5'],
                       ['8','7','6','5','4'],['7','6','5','4','3'],['6','5','4','3','2'],
                       ['5','4','3','2','A']]        
    color,value = toClass(array)
    for i in straightDir:
        i.sort()
    value.sort()
    if value in straightDir:
        return 1
    else :
        return 0
    

def isStraightByIndex(array, subTableType, indexList):#STAIGHT
    # subTableType = 2
    if (int(subTableType) == 1 or int(subTableType) == 2 ):
        straightDir = [['A','K','Q','J','10'],['K','Q','J','10','9'],['Q','J','10','9','8'],
                       ['J','10','9','8','7'],['10','9','8','7','6'],['9','8','7','6','A']]
    else:
        straightDir = [['A','K','Q','J','10'],['K','Q','J','10','9'],['Q','J','10','9','8'],
                       ['J','10','9','8','7'],['10','9','8','7','6'],['9','8','7','6','5'],
                       ['8','7','6','5','4'],['7','6','5','4','3'],['6','5','4','3','2'],
                       ['5','4','3','2','A']]        
    color,value = toClassByIndex(array, indexList)
    for i in straightDir:
        i.sort()
    value.sort()
    if value in straightDir:
        return 1
    else :
        return 0

def isThreeOfKind(array):#THREE_OF_A_KIND
    color,value = toClass(array)
    cnt = []
    for i in setValue(value):
        cnt.append(value.count(i))
    if len(setValue(value)) == 3 :
        if max(cnt) == 3:
            return 1
        else:
            return 0
    else:
        return 0

def isThreeOfKindByIndex(array, indexList):#THREE_OF_A_KIND
    color,value = toClassByIndex(array, indexList)
    cnt = []
    for i in setValue(value):
        cnt.append(value.count(i))
    if len(setValue(value)) == 3 :
        if max(cnt) == 3:
            return 1
        else:
            return 0
    else:
        return 0

def isTwoPairs(array):#TWO_PAIRS
    color,value = toClass(array)
    cnt = []
    for i in setValue(value):
        cnt.append(value.count(i))
    if len(setValue(value)) == 3 :
        if max(cnt) == 2:
            return 1
        else:
            return 0
    else:
        return 0

def isTwoPairsByIndex(array, indexList):#TWO_PAIRS
    color,value = toClassByIndex(array, indexList)
    cnt = []
    for i in setValue(value):
        cnt.append(value.count(i))
    if len(setValue(value)) == 3 :
        if max(cnt) == 2:
            return 1
        else:
            return 0
    else:
        return 0

def isOnePair(array):#PAIR
    color,value = toClass(array)
    if len(setValue(value)) == 4:
        return 1
    else:
        return 0

def isOnePairByIndex(array, indexList):#PAIR
    color,value = toClass(array)
    if len(setValue(value)) == 4:
        return 1
    else:
        return 0

def isHighCard(array):#HIGH_HAND
    return 1

def isHighCardByIndex(array, indexList):#HIGH_HAND
    return 1

def getLevel(array, subTableType, card_compare_type):#获得牌型
    if isRoyalFlush(array) == 1:
        return 9
    if isStraightFlush(array, subTableType) == 1:
        return 8
    if isFourOfKind(array) == 1:
        return 7
    if isFullHouse(array) == 1:
        return 6
    if isFlush(array) == 1:
        return 5
    if isStraight(array, subTableType) == 1:
        return 4
    if isThreeOfKind(array) == 1:
        return 3
    if isTwoPairs(array) == 1:
        return 2
    if isOnePair(array) == 1:
        return 1
    if isHighCard(array) == 1:
        return 0

def getLevelByIndex(array, subTableType, card_compare_type, indexList):#获得牌型
    if isRoyalFlushByIndex(array, indexList) == 1:
        return 9
    if isStraightFlushByIndex(array, subTableType, indexList) == 1:
        return 8
    if isFourOfKindByIndex(array, indexList) == 1:
        return 7
    if isFullHouseByIndex(array, indexList) == 1:
        return 6
    if isFlushByIndex(array, indexList) == 1:
        return 5
    if isStraightByIndex(array, subTableType, indexList) == 1:
        return 4
    if isThreeOfKindByIndex(array, indexList) == 1:
        return 3
    if isTwoPairsByIndex(array, indexList) == 1:
        return 2
    if isOnePairByIndex(array, indexList) == 1:
        return 1
    if isHighCardByIndex(array, indexList) == 1:
        return 0

dirList = { 'A':14, 'K':13, 'Q':12, 'J':11, '10':10, '9':9, '8':8,
            '7':7,  '6':6,  '5':5,  '4':4,  '3':3,   '2':2 }

def compareRoyalFlush(array):#比较皇家同花顺9
    dirRank = []
    for i in array:
        memRank = {}
        memRank['value'] = i
        memRank['rank'] = 1
        dirRank.append(memRank)
    return dirRank
def mapValue(tmp): # 数值映射
    tmp1 = []
    for i in tmp:
        tmp1.append(dirList[i])
    return tmp1

def compareStraightFlush(array):#比较同花顺8或者顺子4
    dirRank = []
    tmp1 = []
    tmp2 = []
    for i in array:
        if 'A' not in i :
            tmp1.append(i)
    cnt = len( tmp1 )
    for i in range( 1, cnt ):
        key = tmp1[i]
        j = i-1
        while j >= 0 and int(min(mapValue(array[j]))) < int(min(mapValue(key))):
            tmp1[j+1] = tmp1[j]
            j -= 1
        tmp1[j+1] = key
    for i in array:
        if 'A' in i and '10' in i:
            tmp2.append(i)
    for i in array:
        if 'A' in i and '2' in i:
            tmp1.append(i)
    tmp1 = tmp2+tmp1
    for i in range(len(tmp1)):
        memRank = {}
        if i > 0:
            if min(mapValue(tmp1[i])) == min(mapValue(tmp1[i-1])) and \
            max(mapValue(tmp1[i])) == max(mapValue(tmp1[i-1])):
                memRank['value'] = tmp1[i]
                memRank['rank'] = dirRank[i-1]['rank']
            else:
                memRank['value'] = tmp1[i]
                memRank['rank'] = dirRank[i-1]['rank']+1   
        else:
            memRank['value'] = tmp1[i]
            memRank['rank'] = 1
        dirRank.append(memRank)
    return dirRank

def compareFourOfKind(array):#比较4条7 或者 葫芦6
    dirRank = []
    tmp = []
    for i in array:
        tmpDir = {}
        tmpDir['value'] = i
        for j in set(i):
            if i.count(j) == 4 or i.count(j) == 3:
                tmpDir['max'] = dirList[j]
            else:
                tmpDir['min'] = dirList[j]
        tmp.append(tmpDir)
    cnt = len(tmp)
    for i in range( 1, cnt ):
        key = tmp[i]
        j = i-1
        while j >= 0 and (tmp[j]['max']<key['max'] or
                        (tmp[j]['max']==key['max'] and tmp[j]['min']<key['min']) ):
            tmp[j+1] = tmp[j]
            j -= 1
        tmp[j+1] = key
    for i in range(cnt):
        memRank = {}
        if i > 0:
            if tmp[i]['max'] == tmp[i-1]['max']  and tmp[i]['min'] == tmp[i-1]['min']:
                memRank['value'] = tmp[i]['value']
                memRank['rank'] = dirRank[i-1]['rank']
            else:
                memRank['value'] = tmp[i]['value']
                memRank['rank'] = dirRank[i-1]['rank']+1   
        else:
            memRank['value'] = tmp[i]['value']
            memRank['rank'] = 1
        dirRank.append(memRank)
    return dirRank

def compareThreeOfKind(array):#比较3条(3) 或者 2对(2)
    dirRank = []
    tmp = []
    cnt = []
    for j in set(array[0]):
        cnt.append(array[0].count(j))
    comType = max(cnt)
    for i in array:
        tmpDir = {}                                                                                                   
        tmpDir['max'] = 0                                                                                             
        tmpDir['mid'] = 0                                                                                             
        tmpDir['min'] = 0 
        tmpDir['value'] = i
        if comType == 3:#比较3条
            for j in set(i):
                if i.count(j) == 3 :
                    tmpDir['max'] = dirList[j]
                else:
                    if tmpDir['mid'] == 0:
                        tmpDir['mid'] = dirList[j]
                    else:
                        if dirList[j] > tmpDir['mid']:
                            key = tmpDir['mid']
                            tmpDir['mid'] = dirList[j]
                            tmpDir['min'] = key
                        else:
                            tmpDir['min'] = dirList[j]
        else:#比较2对
            for j in set(i):
                if i.count(j) == 1 :
                    tmpDir['min'] = dirList[j]
                else:
                    if tmpDir['max'] == 0:
                        tmpDir['max'] = dirList[j]
                    else:
                        if dirList[j] > tmpDir['max']:
                            key = tmpDir['max']
                            tmpDir['max'] = dirList[j]
                            tmpDir['mid'] = key
                        else:
                            tmpDir['mid'] = dirList[j]
        tmp.append(tmpDir)
    cnt = len(tmp)
    for i in range( 1, cnt ):
        key = tmp[i]
        j = i-1
        while j >= 0 and (tmp[j]['max']<key['max'] or
                        (tmp[j]['max']==key['max'] and tmp[j]['mid']<key['mid']) or
                        (tmp[j]['max']==key['max'] and tmp[j]['mid']==key['mid'] and tmp[j]['min']<key['min'])):
            tmp[j+1] = tmp[j]
            j -= 1
        tmp[j+1] = key
    for i in range(cnt):
        memRank = {}
        if i > 0:
            if tmp[i]['max'] == tmp[i-1]['max']  and tmp[i]['mid'] == tmp[i-1]['mid'] and tmp[i]['min'] == tmp[i-1]['min']:
                memRank['value'] = tmp[i]['value']
                memRank['rank'] = dirRank[i-1]['rank']
            else:
                memRank['value'] = tmp[i]['value']
                memRank['rank'] = dirRank[i-1]['rank']+1   
        else:
            memRank['value'] = tmp[i]['value']
            memRank['rank'] = 1
        dirRank.append(memRank)
    return dirRank

def compareOnePair(array):#比较一对1
    dirRank = []
    arrayOld = []
    tmp = []
    for i in array:
        tmpDir = {}
        _dir = {}
        tmpDir['other'] = []
        for j in i :
            tmpDir['value'] = j 
            if i.count(j) == 2 :
                tmpDir['max'] = dirList[j]
            else:
                tmpDir['other'].append(dirList[j])
        tmpDir['other'].sort(reverse=True)
        _dir['value'] = i
        _dir['sort'] = tmpDir
        tmp.append(tmpDir)
        arrayOld.append(_dir)
    cnt = len(tmp)
    for i in range( 1, cnt ):
        key = tmp[i]
        j = i-1
        while j >= 0 and (tmp[j]['max']<key['max'] or
                        (tmp[j]['max']==key['max'] and tmp[j]['other']<key['other'])) :
            tmp[j+1] = tmp[j]
            j -= 1
        tmp[j+1] = key
    for i in range(len(tmp)):
        memRank = {} 
        if i > 0:
            if tmp[i]['max'] == tmp[i-1]['max']  and tmp[i]['other'] == tmp[i-1]['other'] :
                memRank['value'] = tmp[i]
                memRank['rank'] = dirRank[i-1]['rank']
            else:
                memRank['value'] = tmp[i]
                memRank['rank'] = dirRank[i-1]['rank']+1   
        else:
            memRank['value'] = tmp[i]
            memRank['rank'] = 1
        dirRank.append(memRank)
    for i in range(len(dirRank)):
        for j in arrayOld:
            if dirRank[i]['value'] == j['sort']:
                dirRank[i]['value'] = j['value']
    return dirRank
        
def compareHighCard(array):#比较高牌0 或者 同花5
    dirRank = []
    arrayNew = []
    arrayOld = []
    for i in array:
        tmp = []
        _dir = {}
        _dir['value'] = i
        for j in i :
            tmp.append(dirList[j])
        tmp.sort(reverse=True)
        _dir['sort'] = tmp
        arrayOld.append(_dir)
        arrayNew.append(tmp)
    arrayNew.sort(reverse=True)
    for i in range(len(arrayNew)):
        memRank = {}   
        if i > 0:
            if arrayNew[i] == arrayNew[i-1]:
                memRank['value'] = arrayNew[i]
                memRank['rank'] = dirRank[i-1]['rank']
            else:
                memRank['value'] = arrayNew[i]
                memRank['rank'] = dirRank[i-1]['rank']+1   
        else:
            memRank['value'] = arrayNew[i]
            memRank['rank'] = 1
        dirRank.append(memRank)
    for i in range(len(dirRank)):
        for j in arrayOld:
            if dirRank[i]['value'] == j['sort']:
                dirRank[i]['value'] = j['value']
               
    return dirRank


def compare(array, comType, card_compare_type):
    Plist = []
    for i in array:
        color, value = toClass(i['value'])
        Plist.append(value)
    if comType == 9:
        return compareRoyalFlush(Plist)
    if comType in (4, 8):
        return compareStraightFlush(Plist)
    if comType in (7,):
        return compareFourOfKind(Plist)
    if comType in (6,):
        return compareFourOfKind(Plist)
    if comType in (2, 3):
        return compareThreeOfKind(Plist)    
    if comType == 1:
        return compareOnePair(Plist)
    if comType in (0, ):
        return compareHighCard(Plist)
    if comType in (5, ):
        return compareHighCard(Plist)

def getList( Array , totalCards = 7):
    ''' C5/7 算法 ''' 
    Slist = Array
    Plist = [ 1, 1, 1, 1, 1, 0, 0 ]
    Presult = []
    m = totalCards
    n = 5
    while(1):
        Presult.append( getArray(Slist, Plist) )
        if Plist.index(1) == m-n:
            break
        else :
            for i in range(m-1):
                if Plist[i] == 1 and Plist[i+1] == 0:
                    Plist[i] = 0
                    Plist[i+1] = 1
                    cnt = Plist[:i].count(1)
                    for j in  range(cnt):
                        Plist[j] = 1
                    for k in range(i-cnt):
                        Plist[cnt+k] = 0
                    break    
    return Presult

def getListIndex():
    Presult = [[0, 0, 1, 1, 1, 1, 1], [0, 1, 0, 1, 1, 1, 1], [0, 1, 1, 0, 1, 1, 1], [0, 1, 1, 1, 0, 1, 1], [0, 1, 1, 1, 1, 0, 1], [0, 1, 1, 1, 1, 1, 0], [1, 0, 0, 1, 1, 1, 1], [1, 0, 1, 0, 1, 1, 1], [1, 0, 1, 1, 0, 1, 1], [1, 0, 1, 1, 1, 0, 1], [1, 0, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1, 1], [1, 1, 0, 1, 0, 1, 1], [1, 1, 0, 1, 1, 0, 1], [1, 1, 0, 1, 1, 1, 0], [1, 1, 1, 0, 0, 1, 1], [1, 1, 1, 0, 1, 0, 1], [1, 1, 1, 0, 1, 1, 0], [1, 1, 1, 1, 0, 0, 1], [1, 1, 1, 1, 0, 1, 0], [1, 1, 1, 1, 1, 0, 0]]
    return Presult

def getResultByIndex( Array, listIndex, maxtype=0, subTableType=0, card_compare_type = 0):
    '''获取最大的牌'''
    Plist = []
    Mlist = []
    Slist = []
    tmp = {}
    index = 0
    for i in listIndex:
        tmp = {}
        tmp['value'] = i
        tmp['level'] = getLevel(getArray(Array, i), subTableType, card_compare_type)
        tmp['rank'] = 1
        Plist.append(tmp)
        if index > 0:
            key = tmp
            j = index-1
            while j >= 0:
                if int(Plist[j]['level'])<int(key['level']):
                    Plist[j+1] = Plist[j]
                    j -= 1
                else:
                    break
            Plist[j+1] = key
        index = index+1
    cnt = len(Plist)

    for i in range(1,cnt):
        if  Plist[i]['level'] !=  Plist[i-1]['level']:
            Plist[i]['rank'] = 2
            break
    for i in range(cnt):
        if Plist[i]['rank'] == 1:
            Mlist.append(Plist[i])
        else:
            break
    for m in Mlist:
        m['value'] = getArray(Array, m['value'])
    tpMlistLen = len(Mlist)
    if  tpMlistLen > 1:
        Nlist = []
        mid  = compare(Mlist, Mlist[0]['level'], card_compare_type)
        for i in  mid:
            if i['rank'] == 1:
                Nlist.append(i)
        tpNListCt = len(Nlist)
        if (tpNListCt > 0):
            for i in Mlist:
                color, value = toClass(i['value'])
                if  value == Nlist[0]['value']:
                    Slist.append(i['value'])
        else:
            Slist.append(Mlist[0]['value'])
   
    else:
        Slist.append(Mlist[0]['value'])

    if maxtype == 1:
        Slist = Slist[0]
    return Slist

def getArray( Array, Plist ):
    ''' 从7张牌中选择5张 '''
    
    result = []
    for i in range(len(Plist)):
        if Plist[i] == 1 :
            result.append( Array[i] )
                
    return result
    
def toTransform( Array ):
    '''转化牌的格式 ''' 
    
    # 传入的格式：{ 
    #                   K.COMMUNITY_CARDS :['1_2','1_3'....], 
    #                   '2001' :[ { '200F' : 3 , '201C' : [] }, ]  
    #             }
    
    
    # 传出的格式: [
    #                 {  '200F': 0, 
    #                    '201C': 
    #                        [ {'color': '2', 'value': '8'}, ] 5张公共牌 + 2张手牌
    #                 }, 
    #                 
    #                 {
    #                 
    #                 },
    #             ]
    
    desk_cards = []
    for i in Array[ '200B' ]:
        dirCard = {}
        dirCard['color'] = i.split('_')[0]
        dirCard['value'] = i.split('_')[1]
        desk_cards.append( dirCard )
    user_cards = []
    
    for i in Array[ '2001' ]:
        dirUser = {}
        dirUser[ '200F' ] = i[ '200F' ] 
        user_pk = []
        for j in i[ '201C' ]:
            dirUserCard = {}
            dirUserCard['color'] = j.split('_')[0]
            dirUserCard['value'] = j.split('_')[1]  
            user_pk.append(dirUserCard)
            
        dirUser[ '201C' ] = user_pk + desk_cards
        
        user_cards.append(dirUser)
           
    return user_cards

def toCombine( card_list ):
    '''反转化牌的格式'''
    
    # 传入的格式：{ 
    #                   [ {'color': '3', 'value': 'J'}, 
    #                     {'color': '0', 'value': 'J'}, 
    #                     {'color': '1', 'value': 'K'}, ...
    #                   ]
    #             }    
    
    # 传出的格式: ['3_J', '0_J', '1_K', '3_K', '0_9']


    new_card = []
    for card in card_list:
        tmp_str = card['color'] + '_' + card[ 'value' ]
        new_card.append( tmp_str )
    
    return new_card         
        
   
def generationUserMax( Array , subTableType = 0, totalCards = 7, card_compare_type = 0):
    '''根据用户的牌和桌牌进行比较大小'''
    
    # 传入的格式：{ 
    #                   K.COMMUNITY_CARDS :['1_2','1_3'....], 
    #                   '2001' :[ { '200F' : 3 , '201C' : [] }, ]  
    #             }
    
    # 传出的格式: { 
    #                  '200F'   : , 
    #                  '2020' : ,
    #                  '2021'  : , 
    #             }
    # 把用户的牌进行格式化 
    user_cards = toTransform( Array )
    
    # 存放用户的座位号
    user_new   = []
    
    # 存放用户的最大牌
    user_array = []
    
    # 存放返回结果
    user_list  = []
    for i in user_cards:
        
        dirUser = {}
        
        dirUser[ '200F' ] = i[ '200F' ]
        
        # 获取 用户牌 + 公共牌以后的最大牌
        user_max = getResult( getList(i[ '201C' ], totalCards), 1 , subTableType, card_compare_type)
        # user_max = getResultByIndex(i[ '201C' ], getListIndex(), 1)
        # return {}
        dirUser[ '201C' ] = user_max
        
        user_new.append(dirUser)
        
        user_array.append(user_max)
    # 牌中最大的牌
    orderMax = getResult(user_array, 0)
    result_max = orderMax[0]
    for i in user_new:
        
        # 只有皇家同花顺，同花顺和同花，需要比较花色和值，其他的牌型只需要比较牌值即可
        tmp_list = ( 9, 8, 5)
        # 花式进行特殊处理
        # if str(card_compare_type) == '2':
        #     tmp_list = ( Config.ROYAL_FLUSH, Config.STRAIGHT_FLUSH, Config.BOAT_OR_FULL_HOUSE)

        if getLevel( result_max, subTableType, card_compare_type) not in tmp_list:
            
            # 取最大牌的值
            tmp_max   = getPokerValue( result_max )
            
            # 取用户最大牌的值
            user_max  = getPokerValue( i[ '201C' ] )
            
            if equalWithoutOrder( tmp_max, user_max ) and i[ '200F' ] not in user_list:
                winner_info = { 
                                  '200F'   : i[ '200F' ], 
                               }
                user_list.append( winner_info ) 
                 
        # 剩余的牌型则需要比较牌的花色和值
        else:
            if equalWithoutOrder( i[ '201C' ], result_max ) and i[ '200F' ] not in user_list:
            
                winner_info = { 
                                  '200F'   : i[ '200F' ], 
                               }
                user_list.append( winner_info ) 
    return user_list

def equalWithoutOrder( Array_A, Array_B ):
    '''数组无序比较'''
    Array_A.sort()
    Array_B.sort()

    if Array_A == Array_B:
        return True
    else:
        return False

def getResult( Array, maxtype=0, subTableType=0, card_compare_type = 0):
    '''获取最大的牌'''
    Plist = []
    Mlist = []
    Slist = []
    tmp = {}

    index = 0
    for i in Array:
        tmp = {}
        tmp['value'] = i
        tmp['level'] = getLevel(i, subTableType, card_compare_type)
        tmp['rank'] = 0
        Plist.append(tmp)
        if index > 0:
            key = tmp
            j = index-1
            while j >= 0:
                if int(Plist[j]['level'])<int(key['level']):
                    Plist[j+1] = Plist[j]
                    j -= 1
                else:
                    break
            Plist[j+1] = key
        index = index+1
    cnt = len(Plist)
    # print('Plist ======> '+str(Plist))
    # print('')
    for i in range(cnt):
        if i > 0:
            if  Plist[i]['level'] ==  Plist[i-1]['level']:
                Plist[i]['rank'] = Plist[i-1]['rank']
            else:
                Plist[i]['rank'] = Plist[i-1]['rank'] + 1
                break
        else:
            Plist[i]['rank'] = 1
    for i in range(cnt):
        if Plist[i]['rank'] == 1:
            Mlist.append(Plist[i])
        else:
            break
    # print('Plist ======> '+str(Plist))
    # print('')
    # print('Mlist ======> '+str(Mlist))
    # print('')
    tpMlistLen = len(Mlist)
    if  tpMlistLen > 1:
        Nlist = []
        mid  = compare(Mlist, Mlist[0]['level'], card_compare_type)
        for i in  mid:
            if i['rank'] == 1:
                Nlist.append(i)
        tpNListCt = len(Nlist)
        if (tpNListCt > 0):
            for i in Mlist:
                color, value = toClass(i['value'])
                if  value == Nlist[0]['value']:
                    Slist.append(i['value'])
        else:
            Slist.append(Mlist[0]['value'])
   
    else:
        Slist.append(Mlist[0]['value'])
    # print('Slist ======> '+str(Slist))
    # print('')
    if maxtype == 1:
        Slist = Slist[0]
    return Slist



def getPokerValue( Array ):
    '''获取牌的值'''
    tmp_list = []
    for single_poker in Array:
        tmp_list.append( single_poker['value'] )
    return tmp_list


def singleCompare( user_cards ):
    '''比较单张牌的大小'''
    
    # 区分花色
    
    chars = {'J':'11', 'Q':'12', 'K':'13', 'A':'14'}
    formated_cards = {}
    for k in user_cards.keys():
        tmp = user_cards[k].split('_')
        tmp[1] = chars.get(tmp[1], tmp[1])
        formated_cards[k] = int(tmp[0]) + 1000*int(tmp[1])

    _max = 0
    max_user = ''
    for k in formated_cards.keys():
        if formated_cards[k] > _max:
            _max = formated_cards[k]
            max_user = k
    
    return max_user

def generateWiner(Array, index, win_ratio, public_num = 5):
    tmp_cardlist = copy.deepcopy(cardlist)
    for i in range(public_num):
        Array['200B'].append('')
    for j in range(int(run_num/thread_num)):
        random.seed( time.time() )
        cyc_num = (int(10*random.random())%3)+1
        for i in range(cyc_num):
            random.shuffle(tmp_cardlist)
    
        for i in range(public_num):
            # single_card = tmp_cardlist.pop(0)
            single_card = tmp_cardlist[i]
            Array['200B'][5-public_num+i] = single_card
            # tmp_cardlist.append(single_card)

        result = generationUserMax(Array)
        win_num = len(result)

        for i in range(len(result)):
            x = index*run_num/thread_num+j
            y = int(result[i]['200F'])-1
            win_ratio[x][y] = win_ratio[x][y]+1.0/win_num

def counter(Array):
    Array = eval(Array)
    # logging.jsinfo('input:'+str(Array))
    start_time = time.time()
    player_num = len(Array['2001'])
    win_ratio = [[0 for x in range(player_num)] for y in range(run_num)] 

    initCardList()
    for i in range(len(cardlist)-1, -1, -1):

        if cardlist[i] in cardFilterList6_1:
            cardlist.pop(i)
            continue
        if cardlist[i] in Array['200B']:
            cardlist.pop(i)
            continue
        for k in range(len(Array['2001'])):
            if cardlist[i] in Array['2001'][k]['201C']:
                cardlist.pop(i)

    # logging.jsinfo('cardlist is:'+str(cardlist))
    # logging.jsinfo('cardnum is:'+str(len(cardlist)))
    public_num = 5-len(Array['200B'])
    for j in range(thread_num):
        generateWiner(Array.copy(), j, win_ratio, public_num)
    total_ratio = 0.00001
    data = {}
    data['Players_rate'] = [{'Win':0,'Tie':0,'NLose':0} for x in range(player_num)]
    for i in range(player_num):
        data['Players_rate'][i]['Id'] = str(i+1)
        for j in range(0,run_num):
            if win_ratio[j][i]>0.5:
                data['Players_rate'][i]['Win'] = data['Players_rate'][i]['Win']+win_ratio[j][i]
                data['Players_rate'][i]['NLose'] = data['Players_rate'][i]['NLose']+win_ratio[j][i]
                total_ratio = total_ratio+win_ratio[j][i]
            else:
                if win_ratio[j][i]>0:
                    data['Players_rate'][i]['Tie'] = data['Players_rate'][i]['Tie']+1
                    data['Players_rate'][i]['NLose'] = data['Players_rate'][i]['NLose']+win_ratio[j][i]
                    total_ratio = total_ratio+win_ratio[j][i]

    for i in range(player_num):
        data['Players_rate'][i]['Win'] = str('%.2f' % float(data['Players_rate'][i]['Win']/total_ratio*100))
        data['Players_rate'][i]['Tie'] = str('%.2f' % float(data['Players_rate'][i]['Tie']/total_ratio*100))
        data['Players_rate'][i]['NLose'] = str('%.2f' % float(data['Players_rate'][i]['NLose']/total_ratio*100))
    # print(time.time()-start_time)
    return data['Players_rate']

def getAllCardFromPreflop(card):
    result = ''
    res = card.find('s')
    if res!=-1:
        for i in range(4):
            for j in range(4):
                if i==j:
                    if result=='':
                        result = result+card[0]+card_color[str(i)]+card[1]+card_color[str(j)]
                    else:
                        result = result+','+card[0]+card_color[str(i)]+card[1]+card_color[str(j)]
    else:
        res = card.find('o')
        if res!=-1:
            for i in range(4):
                for j in range(4):
                    if i!=j:
                        if result=='':
                            result = result+card[0]+card_color[str(i)]+card[1]+card_color[str(j)]
                        else:
                            result = result+','+card[0]+card_color[str(i)]+card[1]+card_color[str(j)]
        else:
            for i in range(4):
                for j in range(i+1,4):
                    if result=='':
                        result = result+card[0]+card_color[str(i)]+card[1]+card_color[str(j)]
                    else:
                        result = result+','+card[0]+card_color[str(i)]+card[1]+card_color[str(j)]
    return result

def getAverageEquityFromPreflop(cards): 

    for i in range(len(cards)):
        for j in range(i+1, len(cards)):
            if pfPocketEquity.get(cards[i], 0)<pfPocketEquity.get(cards[j], 0):
                tmp = cards[i]
                cards[i] = cards[j]
                cards[j] = tmp
    print(str(cards))
    averageEquityCards = cards[int(len(cards)/2)]
    print(averageEquityCards)
    return averageEquityCards

def getCardsFromSinglePreflop(card):
    result = []
    res = card.find('s')
    if res!=-1:
        for i in range(4):
            for j in range(4):
                if i==j:
                    tmp = card[0]+card_color[str(i)]+card[1]+card_color[str(j)]
                    result.append(tmp)
    else:
        res = card.find('o')
        if res!=-1:
            for i in range(4):
                for j in range(4):
                    if i!=j:
                        tmp = card[0]+card_color[str(i)]+card[1]+card_color[str(j)]
                        result.append(tmp)
        else:
            for i in range(4):
                for j in range(i+1,4):
                    tmp = card[0]+card_color[str(i)]+card[1]+card_color[str(j)]
                    result.append(tmp)
    return result

def cards2str(cards):
    result = ''
    for card in cards:
        if result=='':
            result = result+card
        else:
            result = result+','+card
    return result

def randomTwoHandCard(cards):
    result = ''
    random.seed( time.time() )
    cyc_num = (int(10*random.random())%3)+1
    for i in range(cyc_num):
        random.shuffle(cards)    
    single_card = cards.pop(0)
    cards.append(single_card)
    result = result+str(single_card)
    single_card = cards.pop(0)
    cards.append(single_card)
    result = result+','+str(single_card)
    return result

def randomHandCard(cards):
    random.seed( time.time() )
    cyc_num = (int(10*random.random())%3)+1
    for i in range(cyc_num):
        random.shuffle(cards)    
    single_card = cards.pop(0)
    cards.append(single_card)
    return single_card

def handFromPokerstove2Mini(hand_cards):
    '''转换牌型asah转为[51,25]'''
    ret = []
    ret.append(int(reverse_cards_transfer[hand_cards[0:2]]))
    ret.append(int(reverse_cards_transfer[hand_cards[2:4]]))
    return ret

def getDiffHandCard(cards, used_cards):
    '''从手牌范围中取中等牌力的手牌，无重复'''
    # 根据牌力排序
    for i in range(len(cards)):
        for j in range(i+1, len(cards)):
            if pfPocketEquity.get(cards[i], 0)<pfPocketEquity.get(cards[j], 0):
                tmp = cards[i]
                cards[i] = cards[j]
                cards[j] = tmp
    # 罗列所有牌型
    all_cards = []
    for card in cards:
        tmp = getCardsFromSinglePreflop(card)
        all_cards.extend(tmp)
    #print(all_cards)
    #开始选手牌
    start = int(len(all_cards)/2)
    step = 0
    while(start>0 and start<len(all_cards)):
        if(start-step)>0:
            current = all_cards[start-step]
            curr = handFromPokerstove2Mini(current)
            if curr[0] not in used_cards and curr[1] not in used_cards:
                used_cards.extend(curr)
                return curr
        if(start+step)<len(all_cards):
            current = all_cards[start-step]
            curr = handFromPokerstove2Mini(current)
            if curr[0] not in used_cards and curr[1] not in used_cards:
                used_cards.extend(curr)
                return curr
        step += 1
    tmp = []
    tmp.append(used_cards[0])
    tmp.append(used_cards[1])
    return
         

if __name__ == '__main__':
    Array = "{'200B': ['2_10', '0_10', '0_6'], '2001': [{'200F': 2, '201C': ['3_A', '2_A']}, {'200F': 1, '201C': ['1_6', '2_6']}]}"
    #result = counter(Array)
    # print(result)
    print("==============>")
    cards = ['AA','AQo', '99']
    #result = getAverageEquityFromPreflop(cards)
    #cards = getCardsFromSinglePreflop(result)
    #print(randomHandCard(cards))
    used_cards = [12, 36]
    print(getDiffHandCard(cards, used_cards))
    #print(handFromPokerstove2Mini('AsKh'))
