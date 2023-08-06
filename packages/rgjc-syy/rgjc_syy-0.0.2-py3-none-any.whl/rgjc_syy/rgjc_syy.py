import pandas as pd
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

def data_process(pp,tt,file_name,sheet_name,type):
    f_name = file_name
    content = pd.read_excel(f_name,sheetname=sheet_name)
    value = content.values
    line_num = value.shape[0]
    t_arr = np.array([])
    p_arr = np.array([])
    def myinterpolation(x1,y1,x2,y2,x):
        return (y1-y2)/(x1-x2)*(x-x1)+y1
    def find_p_postion(arr_p,p):
        for j in range(0,arr_p.shape[0]):
            if p < arr_p[j]:
                return j

    for i in range(2,line_num):
        t_arr = np.append(t_arr,value[i][0])
        p_arr = np.append(p_arr,value[i][1])
    p = pp
    t = tt
    inter_p = np.array([])
    inter_t = np.array([])
    err_p = np.array([])
    err_t = np.array([])
    for i in range(0,p.shape[0]):
        int_t = math.floor(t[i])
        inter_p = np.append(inter_p,myinterpolation(t_arr[int_t],p_arr[int_t],t_arr[int_t+1],p_arr[int_t+1],t[i]))
        pos = find_p_postion(p_arr,p[i])
        inter_t = np.append(inter_t,myinterpolation(p_arr[pos-1],t_arr[pos-1],p_arr[pos],t_arr[pos],p[i]))
        err_p = np.append(err_p,(inter_p[i]-p[i])/inter_p[i])
        err_t = np.append(err_t,(inter_t[i]-t[i])/inter_t[i])
    print(inter_p)
    print(inter_t)
    print(err_p)
    print(err_t)
    plt.subplot(211)
    plt.style.use('classic')
    plt.plot(p,t,marker='*')
    plt.title("P & T")
    plt.xlabel("Absolute Press/Mpa")
    plt.ylabel("Temperature/Celsius")
    plt.savefig("P-T.png",dpi=200)
    plt.show()
    z1 = np.polyfit(np.log(p),np.log(t),1)
    p1 = np.poly1d(z1)
    print(p1)
    yvals = p1(np.log(p))
    plt.subplot(212)
    plt.style.use('classic')
    plt.plot(np.log(p),np.log(t),'>')
    plt.plot(np.log(p),yvals)
    plt.title("P & T (ln)")
    plt.xlabel("Absolute Press/Mpa")
    plt.ylabel("Temperature/Celsius")
    plt.text(0.2,4.4,p1)
    plt.savefig("lnP-T.png",dpi=200)
    plt.show()
    co_134a = [374.183,4057.21,-7.66804,1.84376,-2.70786]
    co_600a = [407.854,3637.49,-6.87455,1.42077,-1.46627]
    co_236fa = [398.070,3180.77,-7.85758,1.82555,-3.04877,-3.50977]
    dict_co = {"R123a":co_134a,"R600a":co_600a,"R236fa":co_236fa}
    co = dict_co[type]
    def p_t(tau):
        return (-co[2]*tau+co[3]*tau**1.5+co[4]*tau**2.5+co[5]*tau**5)/(1-tau)
    input_p = math.log(2.26/22.064)
    num = 1000000
    v1 = 0
    for i in range(p.shape[0]):
        input_p = math.log(p[i]/co[1]/1000)
        for i in range(0,num-1):
            v1 = i/num
            v2 = (i+1)/num
            if (input_p-p_t(v1))*(input_p-p_t(v2))<=0:
                break
        print((1-v1)*co[0]-273.15)
    