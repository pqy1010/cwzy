import numpy as np
from cython.view cimport array as cvarray

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
    res=np.zeros_like(data,dtype=np.double)
    for i in range(len(data)-N,-1,-1):
        res[i]=findmax(data[i:i+N],N)
    return res

# def LLV(data,N):
#     return np.min(data[0:N])

def LLV(double[:] data,N):
    cdef int i
    cdef double[:] res
    res=np.zeros_like(data,dtype=np.double)
    for i in range(len(data)-N,-1,-1):
        res[i]=findmin(data[i:i+N],N)
    return res




