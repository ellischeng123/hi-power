# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
from decimal import *

SPECTRUM = "C:/Users/EC/Downloads/HighPower/spectrum/2023_01_22.txt"
LIV = "C:/Users/EC/Downloads/HighPower/LIV/2023_01_06_14_22_23.csv"

# 比對兩個資料夾下檔案數量，若不相符則不執行並印出警告
# 取得檔案清單後先依檔名也就是時間排序，之後再依順序配對
# 輸出 csv sample:
# 


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getcontext().rounding = ROUND_FLOOR

    lookup_low = int(input('lookup_low: '))
    lookup_high = int(input('lookup_high: '))

    spec = pd.read_csv(filepath_or_buffer=SPECTRUM, skiprows=0)
    spec_max = spec.idxmax().values[0]

    print(f"WL_P: {spec_max}")

    liv = pd.read_csv(filepath_or_buffer=LIV, header=1)
    low = liv.iloc[(liv['L'] - lookup_low).abs().argsort()[:1]]
    high = liv.iloc[(liv['L'] - lookup_high).abs().argsort()[:1]]

    print(f"Low A: {low['A'].values[0]}")
    print(f"High A: {high['A'].values[0]}")
    print(f"Low V: {low['V'].values[0]}")
    print(f"High V: {high['V'].values[0]}")

    slope = (Decimal(high['L'].values[0]) - Decimal(low['L'].values[0])) / \
            (Decimal(high['A'].values[0]) - Decimal(low['A'].values[0]))
    print(f'slope: {slope : .3f}')


