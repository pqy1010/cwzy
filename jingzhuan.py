import tushare as ts
import pandas as pd
import numpy as np
from tongdaxin import EMA as EMA
from tongdaxin import CROSS as CROSS
from tongdaxin import MA  as MA
from tongdaxin import REF as REF
import time




def huiyanKxian(data):
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
    sell=CROSS(X3,X2)
    return buy,sell

def bulaojijie(data):
    CLOSE = data['close']
    HIGH = data['high']
    LOW = data['low']
    OPEN = data['open']
    ABS = np.abs

    WY1001=(2*CLOSE+HIGH+LOW)/3
    WY1002=EMA(WY1001,3)
    WY1003=EMA(WY1002,3)
    WY1004=EMA(WY1003,3)
    XYS0=(WY1004-REF(WY1004,1))/REF(WY1004,1)*100

    XYS1=MA(XYS0,1)
    XYS2=MA(XYS0,2)
    return XYS1,XYS2