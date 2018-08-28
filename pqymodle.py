import pandas as pd
import numpy as np
from tongdaxin import EMA as EMA
from tongdaxin import SMA as SMA
from tongdaxin import CROSS as CROSS
from tongdaxin import MA  as MA
from tongdaxin import REF as REF
from tongdaxin import HHV as HHV
from tongdaxin import LLV as LLV

import requests as req
import json
import time


def cwzy_get_hist_data(id):
    thistime=int(time.time()*1000)
    if id[0:3]=='300'or id[0:3]=='000'or id[0:3]=='002':# 深证
        rtntype = 5
        token = '4f1862fc3b5e77c150a2b985b12db0fd'
        cb = 'jQuery183018506892540538078_'+str(thistime-2000)
        newid = id+'2'
        ktype = 'k'
        authorityType=''
        xiahuaxian = str(thistime-1000)
        urls = r'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=%d&token=%s&cb=%s&id=%s&type=%s&authorityType=%s&_=%s' % (rtntype,token, cb, newid,ktype,authorityType,xiahuaxian)
    elif id[0:3]=='600' or id[0:3]=='601'or id[0:3]=='603': #上证
        rtntype=5
        token='4f1862fc3b5e77c150a2b985b12db0fd'
        cb='jQuery183029016096929456525_'+str(thistime-2000)
        newid=id+'1'
        ktype='k'# 日k线
        xiahuaxian=str(thistime-1000)
        authorityType=''
        urls = r'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=%d&token=%s&cb=%s&id=%s&type=%s&authorityType=%s&_=%s' % (rtntype,token, cb, newid,ktype,authorityType,xiahuaxian)

#     print(urls)
    data=req.get(url=urls)
    data_txt=data.content
#     print(data_txt)
    data_txt=data_txt.decode()
    loc=data_txt.find('({')
#     print(loc)
    data_json=json.loads(data_txt[loc+1:-1])
    data_list=[]
    for i in range(len(data_json['data'])):
        data_list.append(data_json['data'][i].split(","))
        data_list[i].extend([id,data_json['name']])
    data_pd = pd.core.frame.DataFrame(data_list)
    data_pd.rename(columns={0:'date',1:'open',2:'close',3:'high',4:'low',5:'volume',6:'volume_rmb',7:'am',8:'turnoverrate',9:'code',10:'name'},inplace = True)
    data_pd=data_pd[::-1]
    data_pd.reset_index(inplace=True,drop=True)
    data_pd.iloc[-1].loc['am']='0'
    data_pd[['open', 'close','high','low','volume','volume_rmb','turnoverrate']] = data_pd[['open', 'close','high','low','volume','volume_rmb','turnoverrate']].astype(float)
    return data_pd


def bulaojijie_buy_point(S1,S2):
    buy=CROSS(S1,S2)
    return buy

if __name__=='__main__':
    data=cwzy_get_hist_data('600821')
    time.sleep(1)