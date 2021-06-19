import numpy as np
import pandas as pd
import datetime

def makeData(li):         
    ans = []
    count = 0
    lis = list(range(42))
    for i in li:
        df = pd.read_csv("../datas/gaika_data/"+ i +".csv", header=None)[lis]
        if count == 0:
            ans = df
        else:
            ans = pd.concat([ans,df], axis = 1)
        count += 1
    return ans

def rounding(x):
    return round(x, 5)

def diffTarget(target,PERIOD):
    li_target = []
    size = len(target)
    for i in range(size-PERIOD):
        x = target[i]
        y = target[i+PERIOD]
        t = y - x
        li_target.append(t)
    target = list(map(rounding,li_target))
    return target
    
def diffData(data,PERIOD):
    diffs = []
    for i in range(len(data)-PERIOD):
        x = [a-b for (a,b) in zip(data[i+PERIOD],data[i])]
        diffs.append(x)
    diffs = np.array(diffs)
    return diffs
           
def makeTweet(c,t,r,a,tm):
    text = c  + "\n"
    text += str(tm[0]) + "年" + str(tm[1]) + "月" + str(tm[2]) + "日" + str(tm[3]) + "時" + str(tm[4]) + "分" + "\n"
    results = [r[a], r[4 + a], r[8 + a], r[12 + a]]
    r = decision(c,results)
    for i in range(len(t)):
        tw =  t[i] + ":  " + r[i] + "\n"
        text += tw
    return text

def makeBool():
    tm = datetime.datetime.now()
    tm = tm - datetime.timedelta(minutes=tm.minute % 10,seconds=tm.second,microseconds=tm.microsecond)
    tm =tm.strftime('%Y-%m-%d-%H-%M-%S')
    li_tm = list(map(int,tm.split("-")))
    date = datetime.date(li_tm[0],li_tm[1],li_tm[2])
    dayweek = date.strftime('%A')
    boolDay = False
    if dayweek == "Sunday":
        boolDay = False
    elif dayweek == "Saturday" and li_tm[3] > 6:
        boolDay = False
    elif dayweek == "Monday" and li_tm[3] < 6:
        boolDay = False
    else:
        boolDay = True
    return boolDay,tm

def decision(c,x):
    li = [0,0,0,0]
    if c == "USDJPY":
        li = [0.05,0.05,0.05,0.1]
    else:
        li = [0.0005,0.0005,0.0005,0.001]
    results = ["","","",""]
    for i in range(4):
        if li[i] * 2 <= x[i]:
            results[i] = "強い買い"
        elif li[i] * 1 <= x[i] and x[i] < li[i] * 2:
            results[i] = "弱い買い"
        elif li[i] * -1 <= x[i] and x[i] < li[i] * 1:
            results[i] = "変化なし"
        elif li[i] * -2 <= x[i] and x[i] < li[i] * -1:
            results[i] = "弱い売り"
        elif x[i] < li[i] * -2:
            results[i] = "強い売り"
    return results
        

    