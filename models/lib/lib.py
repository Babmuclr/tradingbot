import numpy as np
import pandas as pd
import datetime

def dayweek(x):
    li = x.split("-")
    year = int(li[0])
    month = int(li[1])
    day = int(li[2])
    date = datetime.date(year,month,day)
    dayweek = date.strftime('%A')
    return dayweek

def dayhour(x):
    li = x.split("-")
    dayhour = int(li[3])
    return dayhour

def highlow(x,y):
    if y <= x:
        return 1
    elif x <= -y:
        return -1
    else:
        return 0

def highlow2(x,y):
    if y <= x  and x < 2 * y:
        return 1
    elif 2 * y <= x:
        return 2
    elif -2 * y < x and x <= -y:
        return -1
    elif x <= -2 * y:
        return -2
    else:
        return 0

def highlow3(x,y):
    if 2 * y <=  x:
        return 2
    elif x <= -2 * y:
        return -2
    else:
        return 0
    
def makeTarget(x):
    df = pd.read_csv("../../datas/gaika_data/"+ x +".csv", header=None)
    df["price"] = (df[42] + df[43]) / 2
    target = df["price"].values.tolist()
    day = df[44].values.tolist()
    return target, day

def makeData(li):         
    ans = []
    count = 0
    lis = list(range(42))
    for i in li:
        df = pd.read_csv("../../datas/gaika_data/"+ i +".csv", header=None)[lis]
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
    
def checkDay(datas,targets,day,hour,size):
    data = []
    target = []
    for i in range(size):
        if day[i] == "Sunday":
            continue
        elif day[i] == "Saturday" and hour[i] > 6:
            continue
        elif day[i] == "Monday" and hour[i] < 6:
            continue
        else:
            data.append(datas[i])
            target.append(targets[i])
    return data, target
           
           