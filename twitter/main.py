#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

import lib

import twitter

import torch
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(688, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 128)
        self.fc4 = nn.Linear(128, 8)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x

li_tweet = ["USDJPY","EURUSD","GBPUSD","USDCHF","USDCAD","TRYUSD","AUDUSD","NZDUSD",]

with open("/Users/takumiinui/Desktop/tradingbot/twitter/twitterpass.txt") as f:
    s = f.readlines()
    consumer_key=s[0][:-1]
    consumer_secret=s[1][:-1]
    token=s[2][:-1]
    token_secret=s[3]

auth = twitter.OAuth(consumer_key=consumer_key,
consumer_secret=consumer_secret,
token=token,
token_secret=token_secret)
t = twitter.Twitter(auth=auth)

boolDay, tm = lib.makeBool()
# time.sleep(30)

if boolDay:
    results = []
    data = pd.read_csv("/Users/takumiinui/Desktop/tradingbot/datas/model/twitter.csv",header=None)
    diffs = data.diff(6)
    data = pd.concat([data,diffs],axis=1)
    data = data[~(data.isnull().any(axis=1))]
    data = data.values.squeeze()
    data = torch.Tensor(data)

    model_filename = "/Users/takumiinui/Desktop/tradingbot/models/model.pth"
    model = Model()
    model.load_state_dict(torch.load(model_filename))
    model.eval()
    result = model(data).detach().numpy()
        
    status = lib.makeTweet(result, tm) #投稿するツイート
    t.statuses.update(status=status) #Twitterに投稿
    filename = "/Users/takumiinui/Desktop/tradingbot/datas/tweet_data/tweet.txt"
    with open( filename ,"a",newline="") as f:
        f.write(tm+"\n")
        f.writelines(",".join(result))
    print(status)
