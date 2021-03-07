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
import time as systime

def preprocess(s1_filepath,s2_filepath,s3_filepath,d1_filepath,d2_filepath,d3_filepath,nums):
    """
    处理端到端路径时延
    :param s1_filepath:
    :param s2_filepath:
    :param s3_filepath:
    :param d1_filepath:
    :param d2_file_path:
    :param d3_filepath:
    :param nums:
    :return:
    """
    time = systime.strftime("%Y-%m-%d %H-%M-%S", systime.localtime())
    s1_file = open(s1_filepath,"r")
    s2_file = open(s2_filepath,"r")
    s3_file = open(s3_filepath,"r")
    d1_file = open(d1_filepath,"r")
    d2_file = open(d2_filepath,"r")
    d3_file = open(d3_filepath,"r")
    rst_filepath = "data/rst_path_time"+str(time)+".txt"
    rst_file = open(rst_filepath,"a")


    for id in range(nums):
        s1_line = s1_file.readline()
        rst_s1 = process_line(s1_line)
        while rst_s1 and rst_s1[1] != id:
            s1_line = s1_file.readline()
            rst_s1 = process_line(s1_line)
        if not rst_s1:
            print("id:",str(id),"loss")
            break

        s2_line = s2_file.readline()
        rst_s2 = process_line(s2_line)
        while rst_s2 and rst_s2[1] != id:
            s2_line = s2_file.readline()
            rst_s2 = process_line(s2_line)
        if not rst_s2:
            print("id:", str(id), "loss")
            break

        s3_line = s3_file.readline()
        rst_s3 = process_line(s3_line)
        while rst_s3 and rst_s3[1] != id:
            s3_line = s3_file.readline()
            rst_s3 = process_line(s3_line)
        if not rst_s3:
            print("id:", str(id), "loss")
            break

        d1_line = d1_file.readline()
        rst_d1 = process_line(d1_line)
        while rst_d1 and rst_d1[1] != id:
            d1_line = d1_file.readline()
            rst_d1 = process_line(d1_line)
        if not rst_d1:
            print("id:", str(id), "loss")
            break

        d2_line = d2_file.readline()
        rst_d2 = process_line(d2_line)
        while rst_d2 and rst_d2[1] != id:
            d2_line = d2_file.readline()
            rst_d2 = process_line(d2_line)
        if not rst_d2:
            print("id:", str(id), "loss")
            break

        d3_line = d3_file.readline()
        rst_d3 = process_line(d3_line)
        while rst_d3 and rst_d3[1] != id:
            d3_line = d3_file.readline()
            rst_d3 = process_line(d3_line)
        if not rst_d3:
            print("id:", str(id), "loss")
            break

        p1_time = rst_d1[0] - rst_s1[0]
        p2_time = rst_d2[0] - rst_s2[0]
        p3_time = rst_d3[0] - rst_s3[0]

        rst_file.write(str(p1_time)+" "+str(p2_time)+" "+str(p3_time)+"\n")

    s1_file.close()
    s2_file.close()
    s3_file.close()
    d1_file.close()
    d2_file.close()
    d3_file.close()
    rst_file.close()


def process_line(line_str):
    if not line_str:
        return None
    msgs = line_str.split(":")
    if len(msgs) == 3:
        cap_time, actor, id = msgs
        return float(cap_time), int(id)
    else:
        return None

s1_filepath = "data/send/packet_record2021-03-05 21-35-35.txt"
s2_filepath = "data/send/packet_record2021-03-05 21-35-44.txt"
s3_filepath = "data/send/packet_record2021-03-05 21-35-51.txt"
d1_filepath = "data/receive/d1/packet_record2021-03-05 21-38-11.txt"
d2_filepath = "data/receive/d2/packet_record2021-03-05 21-39-51.txt"
d3_filepath = "data/receive/d3/packet_record2021-03-05 21-41-01.txt"
nums = 50000
preprocess(s1_filepath,s2_filepath,s3_filepath,d1_filepath,d2_filepath,d3_filepath,nums)
