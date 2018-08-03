import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jingzhuan
import time




money=10000
tradelist=pd.Series(index=['code','b_time','b_price','b_money','b_count','owntime','state','earn','s_price'])









def select_golden_data():
    datalist=ts.get_stock_basics()
    datalist=datalist.reset_index()
    stocklist=datalist['code']
    stocknum=len(stocklist)
    buylist=[]
    for i in range(stocknum):
        dayK=ts.get_k_data(stocklist[i])
        dayK=dayK[::-1]
        buy, sell = jingzhuan.huiyanKxian(dayK)
        x1, x2 = jingzhuan.bulaojijie(dayK)
        kongpan = jingzhuan.zhulikongpan(dayK)

        buypoint=int(time.mktime(time.strptime(buy[0], '%Y-%m-%d')))
        nowtime=time.time()
        if nowtime-buypoint<=2*24*3600:


select_golden_data()





a=time.time()
data=ts.get_hist_data('000063') #一次性获取全部日k线数据
print('load data use %f'%(time.time()-a))


a=time.time()
buy,sell=jingzhuan.huiyanKxian(data)
print('huiyankxian use %f'%(time.time()-a))


a=time.time()
x1,x2=jingzhuan.bulaojijie(data)
print('bulaojijie use %f'%(time.time()-a))

a=time.time()
kongpan=jingzhuan.zhulikongpan(data)
print('zhulikongpan use %f'%(time.time()-a))
plt.figure()
plt.plot(kongpan)
plt.show()
a=time.time()
time.sleep(1)