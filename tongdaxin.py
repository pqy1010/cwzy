import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import copy





def MA(data,num):
    w=np.ones(num)/num
    tempdata=copy.deepcopy(data)

    for i in range(0,len(data)-num):
        tempdata[i]=np.dot(w,data[i:i+num])
    return tempdata



def EMA(data,N):
    res=np.zeros(len(data))
    res[-1]=data[-1]
    for i in range(len(data)-2,-1,-1):
        res[i]=(2*data[i]+(N-1)*res[i+1])/(N+1)
    # t = pd.Series(res, index=data.index)
    return res

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
    # t = pd.Series(res, index=data.index)
    return res


def DMA(X,A):
    w=copy.deepcopy(A)
    w=np.where(w>1,1,w)
    tempdata=np.zeros_like(X)
    for i in range(len(X)-2,-1,-1):
        tempdata[i]=X[i]*w[i]+tempdata[i+1]*(1-w[i])
    return tempdata


# SMA(C,N,M)    = M/N*C + (N-M)/N * REF(SMA(C,N,M),1);



# def HHV(data,N):
#     return np.max(data[0:N])


def HHV(data,N):
    res=np.zeros_like(data)
    res[-N:]=data[-N:]
    for i in range(len(data)-N,-1,-1):
        res[i]=data[i:i+N].max()
    return res

# def LLV(data,N):
#     return np.min(data[0:N])

def LLV(data,N):
    res=np.zeros_like(data)
    res[-N:]=data[-N:]
    for i in range(len(data)-N,-1,-1):
        res[i]=data[i:i+N].min()
    return res