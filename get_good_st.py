import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jingzhuan
import time



def get_st():
    st_buy_list=list()
    stlist=ts.get_stock_basics()
    for i in stlist:
