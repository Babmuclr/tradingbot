#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from urllib.request import urlopen
from bs4 import BeautifulSoup

import time
import datetime

DRIVER_PATH = '/Users/takumiinui/Desktop/tradingbot/chromedriver'
url = 'https://widget.oanda.jp/order-book'
li_currency = ["USD / JPY","USD / JPY","XAG / USD","XAU / USD","EUR / USD","EUR / JPY","GBP / JPY","AUD / JPY",
              "GBP / USD","AUD / USD","EUR / AUD","EUR / CHF","EUR / GBP","GBP / CHF","NZD / USD","USD / CAD","USD / CHF"]

li_filename = ["USDJPY","XAGUSD","XAUUSD","EURUSD","EURJPY","GBPJPY","AUDJPY",
              "GBPUSD","AUDUSD","EURAUD","EURCHF","EURGBP","GBPCHF","NZDUSD","USDCAD","USDCHF"]

options = Options()
options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=options)

def getSource(c1, c2):
    element = driver.find_element_by_link_text(c1)
    #画像のリンクをクリック
    element.click()
    time.sleep(1)
    element = driver.find_element_by_link_text(c2)
    #画像のリンクをクリック
    element.click()
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser") 
    x = soup.find_all("rect", class_="highcharts-point")
    li = []
    for i in x:
        li.append(int(i.get("height")))
    liFill = []
    for i in x:
        liFill.append(i.get("fill"))
    return li, liFill

def makeNewlist(x):
    newList = [0,0,0,0,0,0,0,0]
    newList[0] = x[0]
    newList[7] = x[4]
    newList[2] = x[0]
    newList[5] = x[4]
    newList[1] = x[1] - x[0]
    newList[6] = x[3] - x[4]
    newList[3] = newList[1]
    newList[4] = newList[6]
    return newList

def job():
    driver.get(url)
    time.sleep(5)
    li = []
    liFill = []
    for i in range(len(li_currency)-1):
        a, b = getSource(li_currency[i],li_currency[i+1])
        li.append(a)
        liFill.append(b)
        time.sleep(5)
    driver.quit()

    spaceLi = []
    for i in range(len(liFill)):
        numli = [1,0,0,0,0]
        num = 0
        for j in range(len(liFill[i])-1):
            if liFill[i][j] == liFill[i][j+1]:
                numli[num] += 1
            else:
                num += 1
                numli[num] += 1
        spaceLi.append(numli)
    lisplit = list(map(makeNewlist,spaceLi))
    
    tm = datetime.datetime.now()
    tm = tm - datetime.timedelta(minutes=tm.minute % 10,seconds=tm.second,microseconds=tm.microsecond)
    tm =tm.strftime('%Y-%m-%d-%H-%M-%S')
    print(tm)

    for i in range(len(li_filename)):
        filename = "/Users/takumiinui/Desktop/tradingbot/datas/oanda_data/" + li_filename[i] + ".csv"
        with open( filename ,"a",newline="") as f:
            writer = csv.writer(f)
            data = li[i]
            data.append(tm)
            writer.writerow(data)
        filename2 = "/Users/takumiinui/Desktop/tradingbot/datas/oanda_data/" + li_filename[i] + "split.csv"
        with open( filename2 ,"a",newline="") as f:
            writer = csv.writer(f)
            data = lisplit[i]
            data.append(tm)
            writer.writerow(data)

job()