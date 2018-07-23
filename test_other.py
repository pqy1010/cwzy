import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

def jingzhuan_huiyanKxian(data):
    CLOSE = data['close']
    HIGH = data['high']
    LOW = data['low']
    OPEN = data['open']
    ABS = np.abs
    T = 1
    V1 = ABS((CLOSE * 2 + HIGH + LOW) / 4 - MA(CLOSE, 20)) / MA(CLOSE, 20) * T
    X1 = (CLOSE + LOW + HIGH + OPEN) / 4
    X2 = EMA(X1, 5)
    X3 = EMA(X2, 7)
    buy = CROSS(X2, X3)
    return buy


def MA(data, num):
    w = np.ones(num) / num
    return np.convolve(w, data)[:-num + 1]


def EMA(data,N):
    res=np.zeros(len(data))
    for i in range(len(data)-2,-1,-1):
        res[i]=(2*data[i]+(N-1)*res[i+1])/(N+1)
    t = pd.Series(res, index=data.index)
    return t

def CROSS(x1, x2):
    dx = x1 - x2
    loc = []
    for i in range(1, len(dx)):
        if dx[i - 1] < 0 and dx[i] >= 0:
            loc.append(dx.index[i])
    return loc


data=ts.get_hist_data('000063') #一次性获取全部日k线数据
V1=jingzhuan_huiyanKxian(data)
time.sleep(1)