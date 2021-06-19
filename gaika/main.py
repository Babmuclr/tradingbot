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

DRIVER_PATH = '../chromedriver'
url = 'https://www.gaitame.com/markets/tool/'
li_currency = [
    "USDJPY","EURJPY","EURUSD","GBPJPY","CADJPY","CHFJPY","GBPUSD","USDCHF","SEKJPY","NOKJPY",
    "EURGBP","USDCAD","TRYJPY","ZARJPY","MXNJPY","TRYUSD","EURTRY","RUBJPY","AUDJPY","NZDJPY",
    "AUDUSD","NZDUSD","EURAUD","GBPAUD","AUDCAD","EURNZD","AUDNZD","CNYJPY","HKDJPY","SGDJPY"
    ]

options = Options()
options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument('--headless')

def main():
    li_price = [[0 for i in range(2)] for j in range(30)]
    li_sell = [[0 for i in range(21)] for j in range(30)]
    li_buy = [[0 for i in range(21)] for j in range(30)]

    driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=options)
    driver.get(url)
    source = driver.page_source
    soup = BeautifulSoup(source,"html.parser")
    tables = soup.find_all("table")
    res = soup.find_all("dd")

    for i in range(30):
        tx = res[2*i+1].text.split(" ")
        li_price[i][0] = float(tx[0])
        li_price[i][1] = float(tx[2])

    for k in range(30):
        x = tables[k].find_all("td") 
        for i in range(21):
            for j in range(10):
                if x[21*i+j].find("span") == None:
                    continue
                else:
                    li_sell[k][i] += 1
            for j in range(10):
                if x[21*i+j+11].find("span") == None:
                    continue
                else:
                    li_buy[k][i] += 1 

    driver.quit()

    tm = datetime.datetime.now()
    tm = tm - datetime.timedelta(minutes=tm.minute % 10,seconds=tm.second,microseconds=tm.microsecond)
    tm =tm.strftime('%Y-%m-%d-%H-%M-%S')

    for i in range(30):
        filename = "../datas/gaika_data/" + li_currency[i] + ".csv"
        with open( filename ,"a",newline="") as f:
            writer = csv.writer(f)
            data = (li_buy[i] + li_sell[i] + li_price[i])
            data.append(tm)
            writer.writerow(data)

main()