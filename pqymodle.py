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

    if int(id[0])==3:
        rtntype = 5
        token = '4f1862fc3b5e77c150a2b985b12db0fd'
        cb = 'jQuery18307611704805113713_1535357772151'
        newid = 'id'+'2'
        type = 'r'
        iscr = 'false'
        xiahuaxian = '1535357774245'
        urls = r'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=%d&token=%s&cb=%s&id=%s&type=%s&iscr=%s&_=%s' % (rtntype,token, cb, newid,type,iscr,xiahuaxian)
    elif int(id[0])==0 or int(id[0])==6:
        jQ = r'jQuery1830584617836716971_1535355855473'
        token = r'4f1862fc3b5e77c150a2b985b12db0fd'
        urls = r'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=%s&cb=%s&id=%s&type=k&authorityType=&_=1535355856791' % (token, jQ, id)



    data=req.get(url=urls)
    data_txt=data.content
    data_txt=data_txt.decode()
    loc=data_txt.find(jQ)
    data_json=json.loads(data_txt[loc+1:-1])
    data_list=[]
    for i in range(len(data_json['data'])):
        data_list.append(data_json['data'][i].split(","))
        data_list[i].extend([id,data_json['name']])
    data_pd = pd.core.frame.DataFrame(data_list)
    # data_pd.rename(columns={},)
    return data_pd




if __name__=='__main__':
    data=cwzy_get_hist_data('0001121')
    time.sleep(1)
