import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time




def MA(data, num):
    w = np.ones(num) / num
    temp=data.rolling(window=num,center=False).mean()
    # return pd.Series(np.vstack([temp[num-1:],np.zeros(num-1).reshape(-1,1)),index=data.index)
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
        if dx[i - 1] > 0 and dx[i] <= 0:
            loc.append(dx.index[i])
    return loc

def REF(data,N):
    temp=np.zeros_like(data)+0.01
    temp[0:-N]=data[N:]
    return temp


def SMA(data,M,N):
    res=np.zeros(len(data))
    for i in range(len(data)-2,-1,-1):
        res[i]=(M*data[i]+(N-1)*res[i+1])/(N+1)
    t = pd.Series(res, index=data.index)
    return t

def HHV(data,N):
    return np.max(data[0:N+1])

def LLV(data,N):
    return np.min(data[0:N+1])