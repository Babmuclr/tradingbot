# coding: utf-8

import numpy as np
import pandas as pd
import datetime
           
def makeTweet(r, tm):
    li_tweet = ["USDJPY","EURUSD","GBPUSD","USDCHF","USDCAD","TRYUSD","AUDUSD","NZDUSD",]
    text = ""
    # twitterでは、同じtweetをすることができないから、時間を入れることで解決する。
    text += str(tm[0]) + "年" + str(tm[1]) + "月" + str(tm[2]) + "日" + str(tm[3]) + "時" + str(tm[4]) + "分の1時間後予想" + "\n"
    r = decision(r)
    for num, i in enumerate(li_tweet):
        text +=  (i + "：  "+ r[num] + "\n")
    return text

# マーケットが開いているかどうか
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

def decision(x):
    results = ["","","","","","","",""]
    for i, res in enumerate(x):
        if 0.6 <= res:
            results[i] = "強い買い"
        elif 0.3 <= res and res < 0.6:
            results[i] = "弱い買い"
        elif -0.3 <= res and res < 0.3:
            results[i] = "変化なし"
        elif -0.6 <= res and res < -0.3:
            results[i] = "弱い売り"
        elif res < -0.6:
            results[i] = "強い売り"
        else: 
            results[i] = "error"
    return results
        

    