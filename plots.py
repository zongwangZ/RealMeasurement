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
import numpy as np
rst_filepath = "data/rst_path_time2021-03-20 23-11-26.txt"
"""
发包数量不变，变化发包间隔（实质是测量时间增大）
"""
def plot_measuretime(num_packet=6000,interval_list=[1,5,10,20,30,60],sum_packet=360000,ifplot=True):
    """
    观察测量时间的影响
    :param num_packet 发包数量不变，为num_packet
    :param interval_list 每隔多少包，选取一个包，间接为测量的时间
    :param sum_packet 最大测量包数，类似最长测量时间
    :return:
    """
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
        plt.figure()
        for index in range(len(cov12)):
            p12 = cov12[index]
            p13 = cov13[index]
            p23 = cov23[index]
            plt.scatter(index,p12,c="b")
            plt.scatter(index,p13,c="r")
            plt.scatter(index,p23,c="y")
        plt.show()
        plt.close()
    return cov12,cov13,cov23

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
    if num_packet_list is None:
        num_packet_list = [100, 500, 1000, 3000, 6000, 12000, 30000, 40000, 60000, 120000]
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
        plt.figure()
        for index in range(len(cov12)):
            p12 = cov12[index]
            p13 = cov13[index]
            p23 = cov23[index]
            plt.scatter(index, p12, c="b")
            plt.scatter(index, p13, c="r")
            plt.scatter(index, p23, c="y")
        plt.show()
        plt.close()
    return cov12, cov13, cov23

"""
测量时间不变，不同时段测量，观察背景流变化对其影响
"""
def plot_background(num_packet=3000,sum_packet=360000,ifplot=True):
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
    plt.figure()
    for index in range(len(cov12)):
        # for index in range(5):
        p12 = cov12[index]
        p13 = cov13[index]
        p23 = cov23[index]
        plt.scatter(index, p12, c="b")
        plt.scatter(index, p13, c="r")
        plt.scatter(index, p23, c="y")
    plt.show()
    plt.close()


if __name__ == '__main__':
    # plot_measuretime(num_packet=3000)
    # plot_num_packet()
    plot_background(60000)