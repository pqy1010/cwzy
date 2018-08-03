import tushare as ts
import pandas as pd
import numpy as np
from tongdaxin import EMA as EMA
from tongdaxin import SMA as SMA
from tongdaxin import CROSS as CROSS
from tongdaxin import MA  as MA
from tongdaxin import REF as REF
from tongdaxin import HHV as HHV
from tongdaxin import LLV as LLV
# from tdx import HHV as HHV
# from tdx import LLV as LLV
import time




def huiyanKxian(data):
    CLOSE = data['close'].values
    HIGH = data['high'].values
    LOW = data['low'].values
    OPEN = data['open'].values
    ABS = np.abs
    T = 1
    V1 = ABS((CLOSE * 2 + HIGH + LOW) / 4 - MA(CLOSE, 20)) / MA(CLOSE, 20) * T
    X1 = (CLOSE + LOW + HIGH + OPEN) / 4
    X2 = EMA(X1, 5)
    X3 = EMA(X2, 7)

    X2=pd.Series(X2,index=data['date'])
    X3=pd.Series(X3,index=data['date'])
    buy = CROSS(X2, X3)
    sell=CROSS(X3,X2)
    return buy,sell

def bulaojijie(data):
    CLOSE = data['close'].values
    HIGH = data['high'].values
    LOW = data['low'].values
    OPEN = data['open'].values
    ABS = np.abs

    WY1001=(2*CLOSE+HIGH+LOW)/3
    WY1002=EMA(WY1001,3)
    WY1003=EMA(WY1002,3)
    WY1004=EMA(WY1003,3)
    XYS0=(WY1004-REF(WY1004,1))/REF(WY1004,1)*100

    XYS1=MA(XYS0,1)
    XYS2=MA(XYS0,2)

    XYS1=pd.Series(XYS1,index=data['date'])
    XYS2 = pd.Series(XYS2, index=data['date'])
    return XYS1,XYS2


def zhulikongpan(data):
    H=HIGH=data['high'].values
    C=CLOSE = data['close'].values
    L=LOW = data['low'].values
    O=OPEN = data['open'].values
    N=35
    M=35
    N1=3
    a=time.time()
    B1 = (HHV(H, N) - C) / (HHV(H, N) - LLV(L, N)) * 100 - M# 此处慢的原因是H,L等都是pd.Serves,如果只取其值则很快.
    print('B1 use %f' % (time.time() - a))
    a=time.time()
    B2 = SMA(B1, N, 1) + 100
    print('B2 use %f' % (time.time() - a))
    B3 = (C - LLV(L, N)) / (HHV(H, N) - LLV(L, N)) * 100
    B4 = SMA(B3, 3, 1)
    B5 = SMA(B4, 3, 1) + 100
    B6 = B5 - B2
    kongpanchengdu=np.where(B6>N1,B6-N1,0)*2.5
    kongpanchengdu = pd.Series(kongpanchengdu, index=data['date'])
    return kongpanchengdu
