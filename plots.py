#!/usr/bin/env python
# encoding: utf-8
'''
@project : 'RealMeasurement'
@author  : '张宗旺'
@file    : 'plots'.py
@ide     : 'PyCharm'
@time    : '2021'-'03'-'20' '23':'54':'36'
@contact : zongwang.zhang@outlook.com
'''
"""
负责画图
"""
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
import numpy as np
rst_filepath = "data/rst_path_time2021-03-20 23-11-26.txt"
data_path = "data/plots/"
"""
发包数量不变，变化发包间隔（实质是测量时间增大）
"""
def plot_measuretime(num_packet=6000,interval_list=[1,5,10,20,40,60,120],sum_packet=360000,ifplot=True):
    """
    观察测量时间的影响
    :param num_packet 发包数量不变，为num_packet
    :param interval_list 每隔多少包，选取一个包，间接为测量的时间
    :param sum_packet 最大测量包数，类似最长测量时间
    :return:
    """
    pic_path = data_path+"plot_measuretime"+".pdf"
    cov12 = []
    cov13 = []
    cov23 = []
    for index,interval in enumerate(interval_list):
        file = open(rst_filepath, "r")
        id = 0
        i = 0
        p1_times = []
        p2_times = []
        p3_times = []
        line = file.readline()
        while i < num_packet and id <sum_packet:
            id = i * interval
            while line:
                id_, p1_time,p2_time,p3_time = line.split(" ")
                if int(id_) == id:
                    p1_times.append(float(p1_time))
                    p2_times.append(float(p2_time))
                    p3_times.append(float(p3_time))
                    line = file.readline()
                elif int(id_) > id:
                    break
                elif int(id_) < id:
                    line =  file.readline()
            i += 1
        p12 = np.cov(p1_times, p2_times)[0, 1]
        p13 = np.cov(p1_times, p3_times)[0, 1]
        p23 = np.cov(p2_times, p3_times)[0, 1]
        print(p12,p13,p23)
        p12 = np.log10(p12)
        p13 = np.log10(p13)
        p23 = np.log10(p23)
        # p12 = np.log10(-p12)
        # p13 = np.log10(-p13)
        # p23 = np.log10(-p23)
        cov12.append(p12)
        cov13.append(p13)
        cov23.append(p23)
    if ifplot:
        index = list(range(len(interval_list)))
        x_tick = num_packet*np.array(interval_list,dtype=int)/100
        x_tick = [int(i) for i in x_tick]
        plot_general(index,[cov12,cov13,cov23],pic_path=pic_path,
                     x_label="测量时间（秒）",y_label="时延协方差（log10）",
                     lengend_list=["路径12的时延协方差","路径13的时延协方差","路径23的时延协方差"],
                     color_list=["b","r","gray"],xtick=x_tick)


    return cov12,cov13,cov23

def plot_general(x,y_list,pic_path,x_label,y_label,lengend_list,color_list,xtick=None,ytick=None):
    plt.figure()
    for i,y in enumerate(y_list):
        plt.scatter(x, y, c=color_list[i], label=lengend_list[i])

    plt.legend(fontsize=16)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)
    # plt.ylim((-4.8,-4.4),)
    # plt.yticks([-4.8,-4.7,-4.6,-4.5,-4.4])
    plt.xticks(x, xtick,fontsize=16)
    plt.yticks(fontsize=16)
    foo_fig = plt.gcf()  # 'get current figure'
    foo_fig.savefig(pic_path, format='pdf', dpi=1000)
    plt.show()
    plt.close()

"""
测量时间不变，发包数量变化
"""
def plot_num_packet(num_packet_list=None, sum_packet=20 * 60 * 100, ifplot=True):
    """
    观察包数量对测量影响
    :param num_packet_list 发包数量
    :param sum_packet 间接规定了测量时间
    :return:
    """
    pic_path = data_path +"num_packet"+".pdf"
    if num_packet_list is None:
        num_packet_list = [100, 500, 1000, 3000, 6000, 12000, 30000, 60000]
    interval_list = [round(sum_packet/num_packet) for num_packet in num_packet_list]
    cov12 = []
    cov13 = []
    cov23 = []
    for index, interval in enumerate(interval_list):
        file = open(rst_filepath, "r")
        id = 0
        i = 0
        p1_times = []
        p2_times = []
        p3_times = []
        line = file.readline()
        while i < num_packet_list[index] and id < sum_packet:
            id = i * interval
            while line:
                id_, p1_time, p2_time, p3_time = line.split(" ")
                if int(id_) == id:
                    p1_times.append(float(p1_time))
                    p2_times.append(float(p2_time))
                    p3_times.append(float(p3_time))
                    line = file.readline()
                elif int(id_) > id:
                    break
                elif int(id_) < id:
                    line = file.readline()
            i += 1
        p12 = np.cov(p1_times, p2_times)[0, 1]
        p13 = np.cov(p1_times, p3_times)[0, 1]
        p23 = np.cov(p2_times, p3_times)[0, 1]
        print(p12, p13, p23)
        p12 = np.log10(p12)
        p13 = np.log10(p13)
        p23 = np.log10(p23)
        # p12 = np.log10(-p12)
        # p13 = np.log10(-p13)
        # p23 = np.log10(-p23)
        cov12.append(p12)
        cov13.append(p13)
        cov23.append(p23)
    if ifplot:
        x = list(range(len(num_packet_list)))
        x_tick = [i/1000 for i in num_packet_list]
        plot_general(x,[cov12,cov13,cov23],pic_path=pic_path,
                     x_label="探测包数量(1e3)",y_label="时延协方差（log10）",
                     lengend_list=["路径12的时延协方差","路径13的时延协方差","路径23的时延协方差"],
                     color_list=["b","r","gray"],xtick=x_tick)
    return cov12, cov13, cov23

"""
测量时间不变，不同时段测量，观察背景流变化对其影响
"""
def plot_background_traffic(num_packet=60000,sum_packet=360000,ifplot=True):
    file = open(rst_filepath, "r")
    p1_times = []
    p2_times = []
    p3_times = []
    cov12 = []
    cov13 = []
    cov23 = []
    id = 0
    i = 0
    line = file.readline()
    while id < sum_packet:
        i += 1
        id = i * num_packet
        while line:
            id_, p1_time, p2_time, p3_time = line.split(" ")
            if int(id_) < id:
                p1_times.append(float(p1_time))
                p2_times.append(float(p2_time))
                p3_times.append(float(p3_time))
                line = file.readline()
            elif int(id_) >= id:
                break
        p12 = np.cov(p1_times, p2_times)[0, 1]
        p13 = np.cov(p1_times, p3_times)[0, 1]
        p23 = np.cov(p2_times, p3_times)[0, 1]
        print(p12, p13, p23)
        p12 = np.log10(p12)
        p13 = np.log10(p13)
        p23 = np.log10(p23)

        # p12 = np.log10(-p12)
        # p13 = np.log10(-p13)
        # p23 = np.log10(-p23)
        cov12.append(p12)
        cov13.append(p13)
        cov23.append(p23)
        p1_times = []
        p2_times = []
        p3_times = []
    if ifplot:
        pic_path = data_path+"background_traffic"+".pdf"
        x = list(range(1,int(sum_packet/num_packet)+1))
        measuretime = int(num_packet/100)
        x_tick = [measuretime*i for i in x]

        plot_general(x,[cov12,cov13,cov23],pic_path=pic_path,
                     x_label="测量时间段（秒）",y_label="时延协方差（log10）",
                     lengend_list=["路径12的时延协方差","路径13的时延协方差","路径23的时延协方差"],
                     color_list=["b","r","gray"],xtick=x_tick)


if __name__ == '__main__':
    plot_measuretime(num_packet=3000)
    # plot_num_packet(sum_packet=10 * 60 * 100)
    # plot_num_packet(sum_packet=20 * 60 * 100)
    # plot_background_traffic(60000)
    pass