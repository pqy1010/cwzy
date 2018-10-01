import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jingzhuan
import time
from pytdx.hq import TdxHq_API
import sqlite3


money=10000
tradelist=pd.Series(index=['name','code','b_time','b_price','b_money','b_count','owntime','state','earn','s_price','s_time'])
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
        buy, sell,zhicheng,zuli = jingzhuan.huiyanKxian(dayK)
        x1, x2 = jingzhuan.bulaojijie(dayK)
        kongpan = jingzhuan.zhulikongpan(dayK)
        stockinfo={'data':dayK,'buy':buy,'sell':sell,'x1':x1,'x2':x2,'kongpan':kongpan}
        judge_flag=stockjudge(stockinfo)
        if judge_flag==1:
            buylist.append([stocklist[i],datalist['name'][i]])
    return buylist

def buy_precious(buylist):
    pre_num=len(buylist)

def savebuylisttodb(datalist):
    conn = sqlite3.connect('stockinfo.db')
    c = conn.cursor()
    tableres = c.execute('select * from sqlite_master where type=\'table\' and name=\'stockstatus\'')
    tablenum = tableres.fetchall()
    if len(tablenum) == 0:
        print('creat table stockstatus')
        sql = '''create table stockstatus(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                name text,
                code text,
                ctime text,
                b_time text,
                b_price float,
                b_money float,
                b_count int,
                owntime float,
                state text,
                earn float,
                earnrate float,
                s_price float,
                s_time text                
                );'''
        c.execute(sql)
        conn.commit()
    for data in datalist:
        ctime=time.localtime(time.time())
        ctimestr='%d-%d-%d %d:%d:%d'%(ctime.tm_year,ctime.tm_mon,ctime.tm_mday,ctime.tm_hour,ctime.tm_min,ctime.tm_sec)
        c.execute('insert into stockstatus(name,code,state,ctime)values(?,?,?,?) ',(data[1],data[0],'wait buy',ctimestr))
    conn.commit()
    conn.close()
buylist=select_golden_data()
savebuylisttodb(buylist)

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