#!/usr/bin/env python
# encoding: utf-8
'''
@project : 'RealMeasurement'
@author  : '张宗旺'
@file    : 'tracert'.py
@ide     : 'PyCharm'
@time    : '2021'-'03'-'19' '19':'08':'42'
@contact : zongwang.zhang@outlook.com
'''
'''
间隔某段时间查询tracert
'''
import os
import sys
import time
import sched
data_path = "../data/tracert/"
s = sched.scheduler()
from threading import Timer
import datetime

def tracert(host:str,interval,cnt):
    if cnt > 0:
        t = Timer(interval, tracert, (host, interval, cnt - 1))
        t.start()
        start_time = time.time()
        command = f"tracert {host}"
        rst = os.popen(command).read()
        end_time = time.time()
        time_record = "start_time:"+str(start_time)+" "+"end_time:"+str(end_time)+" "+"during:"+str(end_time-start_time)
        print(time_record)
        print(rst)
        filename = data_path+"tracert_"+host.replace(".","-")+"_"+str(cnt)+".txt"
        with open(filename,"w",encoding="utf-8") as f:
            f.write(time_record)
            f.write(rst)


def do_tracert(host,interval,cnt):
    t = Timer(0, tracert, (host, interval, cnt))
    # t = Timer(interval, print_time, (cnt,))
    t.start()


def print_time(cnt):
    if cnt > 0:
        print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        t = Timer(interval, print_time,(cnt - 1,))
        t.start()



if __name__ == '__main__':
    argc = sys.argv
    if len(argc) != 4:
        sys.exit('Usage: python tracert.py host interval(s) cnt')
    else:
        host = argc[1]
        interval = int(argc[2])
        cnt = int(argc[3])
        # host = "1.15.81.154"
        # host = "172.27.90.37"
        # interval = 300
        # interval = 1
        # cnt = 2
        do_tracert(host,interval,cnt)