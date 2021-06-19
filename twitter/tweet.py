import numpy as np
import time
import sys
sys.path.append('../')
from lib import lib

import twitter
import pickle

li_currency = [
    "USDJPY","EURJPY","EURUSD","GBPJPY","CADJPY","CHFJPY","GBPUSD","USDCHF","SEKJPY","NOKJPY",
    "EURGBP","USDCAD","TRYJPY","ZARJPY","MXNJPY","TRYUSD","EURTRY","RUBJPY","AUDJPY","NZDJPY",
    "AUDUSD","NZDUSD","EURAUD","GBPAUD","AUDCAD","EURNZD","AUDNZD","CNYJPY","HKDJPY","SGDJPY"
    ]

li_tweet = ["USDJPY","EURUSD","GBPUSD","AUDUSD"]
li_time = [3,6,12,24]
PERIOD2 = 6 # 変化の間隔

timeli = ["３０分後","１時間後","２時間後","４時間後"]

with open( "./twitterpass.txt" ,"a",newline="") as f:
    li = f.read().splitlines()
    myConsumerKey = li[0]
    myConsumerSecret = li[1]
    myToken = li[2]
    myTokenSecret = li[3]

auth = twitter.OAuth(
    consumer_key=myConsumerKey,
    consumer_secret=myConsumerSecret,
    token=myToken,
    token_secret=myTokenSecret)
t = twitter.Twitter(auth=auth)

boolDay, tm = lib.makeBool()
print(tm)
time.sleep(30)
if boolDay:
    results = []
    for PERIOD in li_time:
        data = lib.makeData(li_currency).values
        diffs = lib.diffData(data,PERIOD2)
        data = data[PERIOD2:]
        data = np.concatenate([data,diffs],1)[max(PERIOD-PERIOD2,0):]
        data = [data[-1]]
        for i in li_tweet:
            filename = "../models/model/" + i + "/r" + str(PERIOD) + "_0.sav"
            model = pickle.load(open(filename, 'rb'))
            result = model.predict(data)
            results.append(result[0])

    results = list(map(lib.rounding,results))
    li_tm = list(map(int,tm.split("-")))

    for i in range(len(li_tweet)):
        time.sleep(5)
        status = lib.makeTweet(li_tweet[i],timeli,results,i,li_tm) #投稿するツイート
        filename = "../datas/tweet_data/" + li_tweet[i] + ".txt"
        with open( filename ,"a",newline="") as f:
            f.write(tm+"\n")
            f.writelines(status)
        t.statuses.update(status=status) #Twitterに投稿
