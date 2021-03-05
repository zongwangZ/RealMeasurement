#!/usr/bin/env python
# encoding: utf-8
'''
@project : 'RealMeasurement'
@author  : '张宗旺'
@file    : 'data_analysis'.py
@ide     : 'PyCharm'
@time    : '2021'-'03'-'03' '16':'43':'24'
@contact : zongwang.zhang@outlook.com
'''
"""
对产生的测量数据文件分析，画图
"""

def preprocess(filepath):
    dat_file = open("data1.dat","a")
    with open(filepath,"r") as f:
        line = f.readline()
        while line:
            msgs = line.split(" ")[-1].split(":")
            if len(msgs) == 4:
                dest, id, start_time, end_time = msgs
                duration = float(end_time)-float(start_time)
                dat_file.write(str(id)+":"+str(duration)+"\n")
            line = f.readline()

    dat_file.close()
preprocess("log/('127.0.0.1', 10002)2021-03-03 16-06-36.log")
