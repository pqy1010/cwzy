import numpy as np


def findmax(double[:] data,N):
    cdef int i
    temp=data[0]
    for i in range(N):
        if data[i]>temp:
            temp=data[i]
    return temp

def findmin(double[:] data,N):
    cdef int i
    temp=data[0]
    for i in range(N):
        if data[i]<temp:
            temp=data[i]
    return temp



def HHV(double[:] data,N):
    cdef int i
    cdef double[:] res
    res=np.zeros_like(data)
    res=data
    for i in range(len(data)-N,-1,-1):
        res[i]=data[i:i+N].max()
    return res

# def LLV(data,N):
#     return np.min(data[0:N])

def LLV(double[:] data,N):
    cdef int i
    cdef double[:] res
    res=np.zeros_like(data)
    res=data
    for i in range(len(data)-N,-1,-1):
        res[i]=data[i:i+N].min()
    return res




