#!/usr/bin/env python
# encoding: utf-8
'''
@project : 'RealMeasurement'
@author  : '张宗旺'
@file    : 'plots_ns3'.py
@ide     : 'PyCharm'
@time    : '2021'-'03'-'22' '20':'47':'32'
@contact : zongwang.zhang@outlook.com
'''
"""
用于ns3中得到的数据画图
"""
from plots import plot_general,data_path
import numpy as np
"""
ns3中的目的节点不协作时候，测量的数据
"""
# 0类型的数据
data_0 = [[0.0008393512228203982, 0.0008648383264601936, 0.0009070112852271151, -1],
[0.00022495074128888357, 0.00023123027925819526, 0.00023562905086408907, -1],
[0.00012364549894452683, 0.00012242188079372002, 0.00011486466056262415, -1],
[0.00011079052374032898, 9.284517832577255e-05, 0.00010798421771561603, -1],
[7.844181775140301e-05, 7.094699085400782e-05, 8.242772834291948e-05, -1],
[7.660612841134408e-05, 8.13393138854291e-05, 8.218790100591226e-05, -1],
[6.869285507333173e-05, 7.224803708616516e-05, 6.776386602828112e-05, 0],]


# 1类型的数据
data_1 =[
[7.976584774234906e-05, 1.2357147561987403e-05, 2.6395960421962927e-05, -1],
[0.00017244275680873973, 1.037248284413061e-05, 1.0108090135842651e-05, 1],
[0.00014546494508960354, 4.3807716411030626e-05, 4.270812568760841e-05, 1],
[0.00010101221553779069, 3.74013642627024e-05, 3.240660880299334e-05, 1],
[9.980998797442316e-05, 4.514469835493612e-05, 4.716760197029674e-05, 1],
[0.00011340655926164777, 3.9275060688606375e-05, 4.134985935489386e-05, 1],
[0.00020267614609081647, 0.00012752428916709672, 0.00013530129871410602, -1],
]

def plot_0(ifplot=True):
    pic_path = data_path+"ns3_scheme2_measure0"+".pdf"
    cov12 = np.array(data_0)[:,0][:-1]
    cov13 = np.array(data_0)[:,1][:-1]
    cov23 = np.array(data_0)[:,2][:-1]
    cov12 = np.log10(cov12)
    cov13 = np.log10(cov13)
    cov23 = np.log10(cov23)
    for i in data_0:
        print(i)
    num_packet = 3000
    if ifplot:
        interval_list = [1, 5, 10, 20, 40, 60]
        index = list(range(len(interval_list)))
        x_tick = num_packet*np.array(interval_list,dtype=int)/100
        x_tick = [int(i) for i in x_tick]
        plot_general(index,[cov12,cov13,cov23],pic_path=pic_path,
                     x_label="测量时间（秒）",y_label="时延协方差（log10）",
                     lengend_list=["路径12的时延协方差","路径13的时延协方差","路径23的时延协方差"],
                     color_list=["b","r","gray"],xtick=x_tick)

def plot_1(ifplot=True):
    pic_path = data_path+"ns3_scheme2_measure1"+".pdf"
    cov12 = np.array(data_1)[:,0][:-1]
    cov13 = np.array(data_1)[:,1][:-1]
    cov23 = np.array(data_1)[:,2][:-1]
    cov12 = np.log10(cov12)
    cov13 = np.log10(cov13)
    cov23 = np.log10(cov23)
    for i in data_1:
        print(i)
    num_packet = 3000
    if ifplot:
        interval_list = [1, 5, 10, 20, 40, 60]
        index = list(range(len(interval_list)))
        x_tick = num_packet*np.array(interval_list,dtype=int)/100
        x_tick = [int(i) for i in x_tick]
        plot_general(index,[cov12,cov13,cov23],pic_path=pic_path,
                     x_label="测量时间（秒）",y_label="时延协方差（log10）",
                     lengend_list=["路径12的时延协方差","路径13的时延协方差","路径23的时延协方差"],
                     color_list=["b","r","gray"],xtick=x_tick)

if __name__ == '__main__':
    plot_0()
    plot_1()