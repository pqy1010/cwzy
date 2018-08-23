import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jingzhuan
import time
from pytdx.hq import TdxHq_API



money=10000
tradelist=pd.Series(index=['code','b_time','b_price','b_money','b_count','owntime','state','earn','s_price'])
# ownlist=pd.DataFrame(index=['code',''])
def stockjudge(info):
    buypoint = int(time.mktime(time.strptime(info['buy'][0], '%Y-%m-%d')))
    # nowtime = time.time()
    nowtime=int(time.mktime(time.strptime(time.strftime('%Y-%m-%d'),'%Y-%m-%d')))
    diffx1x2=info['x1']-info['x2']
    if nowtime - buypoint <= 3 * 24 * 3600:
        if info['kongpan'][0] > 0:
            if diffx1x2[0]>=0:
                return 1
    return 0

def select_golden_data():
    datalist=ts.get_stock_basics()
    datalist=datalist.reset_index()
    stocklist=datalist['code']
    stocknum=len(stocklist)

    buylist=[]
    for i in range(stocknum):
        dayK=ts.get_k_data(stocklist[i])
        dayK=dayK[::-1]
        if dayK.shape[0]<=60:
            continue
        buy, sell = jingzhuan.huiyanKxian(dayK)
        x1, x2 = jingzhuan.bulaojijie(dayK)
        kongpan = jingzhuan.zhulikongpan(dayK)
        stockinfo={'data':dayK,'buy':buy,'sell':sell,'x1':x1,'x2':x2,'kongpan':kongpan}
        judge_flag=stockjudge(stockinfo)
        if judge_flag==1:
            buylist.append(stocklist[i])
    return buylist

def buy_precious(buylist):
    pre_num=len(buylist)



buylist=select_golden_data()


## test code------------------------------------------------------

#
# a=time.time()
# data=ts.get_hist_data('000063') #一次性获取全部日k线数据
# print('load data use %f'%(time.time()-a))
#
#
# a=time.time()
# buy,sell=jingzhuan.huiyanKxian(data)
# print('huiyankxian use %f'%(time.time()-a))
#
#
# a=time.time()
# x1,x2=jingzhuan.bulaojijie(data)
# print('bulaojijie use %f'%(time.time()-a))
#
# a=time.time()
# kongpan=jingzhuan.zhulikongpan(data)
# print('zhulikongpan use %f'%(time.time()-a))
# plt.figure()
# plt.plot(kongpan)
# plt.show()
# a=time.time()
# time.sleep(1)