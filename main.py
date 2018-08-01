import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jingzhuan
import time






a=time.time()
data=ts.get_hist_data('000063') #一次性获取全部日k线数据
print('load data use %f'%(time.time()-a))
a=time.time()
buy,sell=jingzhuan.huiyanKxian(data)
print('huiyankxian use %f'%(time.time()-a))
a=time.time()
x1,x2=jingzhuan.bulaojijie(data)
print('bulaojijie use %f'%(time.time()-a))
kongpan=jingzhuan.zhulikongpan(data)
plt.figure()
plt.plot(kongpan)
plt.show()
a=time.time()
time.sleep(1)