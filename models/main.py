import numpy as np 
import pandas as pd 
import pickle 

import torch
import torch.nn as nn

li_currency = ["USDJPY","EURUSD","GBPUSD","USDCHF","USDCAD","TRYUSD","AUDUSD","NZDUSD",]
DATA_FILE_NAME = "./data_hour.csv"

parser = argparse.ArgumentParser(description='Parse command line options.')

parser.add_argument(
    '-c',
    '--currency',
    type = str,
    help = 'predict currecncy name',
    required = False
)

parser.add_argument(
    '-l',
    '--learning',
    type = str,
    help = 'training mode',
    required = False
)

parser.add_argument(
    '-c',
    '--cuda',
    type = str, 
    help = "cuda name",
    required = True
)

options = parser.parse_args()
device = torch.device(options.cuda if torch.cuda.is_available() else 'cpu')

def columns():
    columns = []
    for i in li_currency:
        column_name = [i + "_" + str(j) for j in range(45)]
        columns += (column_name[:42] + [i + "_price"])
    columns += [i + "_diff" for i in columns]
    return columns

def target_columns():
    columns = []
    for i in li_currency:
        columns += ([i + "_price_target"])
    return columns

df = pd.read_csv(DATA_FILE_NAME)

data = df[columns()] # 予測に必要なインプットのデータ
df_target = df[target_columns()] # ターゲット群

