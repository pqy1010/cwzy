import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jingzhuan
import time
import pqymodle


code='600812'
dayK=pqymodle.cwzy_get_hist_data(code)
buy, sell,zhicheng,zuli = jingzhuan.huiyanKxian(dayK)
K,D,J=pqymodle.KDJ(dayK)
time.sleep(1)