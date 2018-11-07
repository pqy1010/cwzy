import requests as req
import json
import time
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import copy


def one_vote_judge(fhr, fm, fileid, score):
    if len(fhr) <= 60:
        return 11
    orifhr = copy.copy(fhr)
    fhr = rebulitfhr(fhr)
    valiatefhr = np.where(fhr > 240, 0, fhr)
    valiatefhr = np.take(valiatefhr, np.where(valiatefhr != 0)).flatten()
    diff_fhr = np.abs(np.diff(valiatefhr))

    # 胎心率出现跳变,则判断跳变两边胎心率均值是否相差很大.
    jump_fhr_list = np.where(diff_fhr >= 25)[0]
    if len(jump_fhr_list) != 0:
        for jump_fhr in jump_fhr_list:
            mean1 = np.mean(valiatefhr[0:jump_fhr])
            var1 = np.var(valiatefhr[0:jump_fhr])
            mean2 = np.mean(valiatefhr[jump_fhr:])
            var2 = np.mean(valiatefhr[jump_fhr:])
            if abs(mean1 - mean2) > 10:
                return 10
    #         for jump_fhr in jump_fhr_list:
    #             if abs(np.mean(valiatefhr[0:jump_fhr])-np.mean(valiatefhr[jump_fhr:]))>10:
    #                 if score>8:
    #                     print(fileid)
    #                     plt.figure()
    #                     plt.plot(fhr)
    #                     plt.title(str(fileid))
    #                     plt.show()
    #                 return 10
    # 有效胎心率长度小于10min
    if len(valiatefhr) <= 10 * 60:
        #         if score>8:
        #             print(fileid)
        #             plt.figure()
        #             plt.plot(fhr)
        #             plt.title(str(fileid))
        #             plt.show()
        return 11
    # 算出率小于0.7
    if len(valiatefhr) / len(orifhr) <= 0.6:
        return 12

    fm_num = len(fm)
    if fm_num <= 5:
        return 13

    if len(fhr) <= 600:
        return 14

    if len(fhr) >= 1200:
        fhr20min = fhr[0:1200]
    else:
        fhr20min = fhr
    valiatefhr20min = np.where(fhr20min > 240, 0, fhr20min)
    valiatefhr20min = np.take(valiatefhr20min, np.where(valiatefhr20min != 0)).flatten()
    if len(valiatefhr20min) / len(fhr20min) <= 0.6:
        return 15

    # 胎心率>170 的累计时间长>600s
    fhr170len = len(np.where(valiatefhr >= 170)[0])
    if fhr170len >= 600:
        return 16
    # 胎心率>190 的累计时间长>40s
    fhr190len = len(np.where(valiatefhr >= 190)[0])
    if fhr190len >= 40:
        return 17

    fhr110len = len(np.where(valiatefhr <= 110)[0])
    if fhr110len >= 60:
        return 18

    fhr100len = len(np.where(valiatefhr <= 100)[0])
    if fhr100len >= 3:
        return 19
    return 1


def rebulitfhr(originfhr):
    rebuildfhr = originfhr.astype(np.float)
    rebuildfhr = np.where(rebuildfhr > 240, 0, rebuildfhr)

    # linear interpolation

    if rebuildfhr[0] == 0:
        rebuildfhr[0] = originfhr[0]
    if rebuildfhr[-1] == 0:
        rebuildfhr[-1] = originfhr[-1]
    interp_start = 0
    interp_end = 0
    interp_start_value = 0
    interp_end_value = 0
    interp_flag = 0
    originfhrlen = len(rebuildfhr)
    for i in range(originfhrlen - 1):
        if (rebuildfhr[i] != 0 and rebuildfhr[i + 1] == 0):
            interp_start = i
            interp_start_value = rebuildfhr[i]

        if (rebuildfhr[i] == 0 and rebuildfhr[i + 1] != 0):
            interp_end = i + 1
            interp_end_value = rebuildfhr[i + 1]
            interp_flag = 1

        if interp_flag == 1:
            if interp_end - interp_start <= 10:
                temp_interp = np.interp(np.arange(interp_start, interp_end + 1, 1),
                                        np.array([interp_start, interp_end]),
                                        np.array([interp_start_value, interp_end_value]))
                rebuildfhr[interp_start:interp_end + 1] = temp_interp

            interp_flag = 0
    return rebuildfhr.flatten()


path='/home/peng/Redman/Redman/Drgeng/'
filelist=os.listdir(path=path)
out_info=[]
for fileid in filelist:
#     try:
    filepath=path+fileid
    fid=open(filepath,'r',encoding='utf-8')
    datastr=json.load(fid)
    fid.close()
    data=json.loads(datastr)
    if 'fhr' not in data.keys():
#         print('%s has no fhr'%fileid)
        continue
    fhr=np.array(data['fhr'])
    fm=data['fm']
    doctor_score=data['doctor_score']

    one_vote_res=one_vote_judge(fhr,fm,fileid,doctor_score)
    out_info.append([doctor_score,one_vote_res,data['id']])