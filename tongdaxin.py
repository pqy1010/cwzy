import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time




def MA(data, num):
    if num==1:
        return data
    w = np.ones(num) / num
    # temp=data.rolling(window=num,center=False).mean()
    # return pd.Series(np.vstack([temp[num-1:],np.zeros(num-1).reshape(-1,1)),index=data.index)
    temp=np.convolve(w, data)[0:-num + 1]
    temp=np.roll(temp,-1)
    return pd.Series(temp,index=data.index)

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


def SMA(data,N,M):
    res=np.zeros(len(data))
    res[-1]=data[-1]
    for i in range(len(data)-2,-1,-1):
        res[i]=(M*data[i]+(N-M)*res[i+1])/(N)
    t = pd.Series(res, index=data.index)
    return t

# SMA(C,N,M)    = M/N*C + (N-M)/N * REF(SMA(C,N,M),1);



# def HHV(data,N):
#     return np.max(data[0:N])
def HHV(data,N):
    res=np.zeros_like(data)
    res[-N:]=data[-N:]
    for i in range(len(data)-N,-1,-1):
        res[i]=np.max(data[i:i+N])
    return res

# def LLV(data,N):
#     return np.min(data[0:N])

def LLV(data,N):
    res=np.zeros_like(data)
    res[-N:]=data[-N:]
    for i in range(len(data)-N,-1,-1):
        res[i]=np.min(data[i:i+N])
    return res