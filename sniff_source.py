#!/usr/bin/env python
# encoding: utf-8
'''
@project : 'RealMeasurement'
@author  : '张宗旺'
@file    : 'sniff_source'.py
@ide     : 'PyCharm'
@time    : '2021'-'03'-'05' '17':'06':'05'
@contact : zongwang.zhang@outlook.com
'''

"""
用于抓包
"""
from scapy.all import *
import sys

import time as systime

class Sniff:
    def __init__(self,iface,filter,count,timeout):
        self.iface = iface
        self.filter = filter
        self.count = count
        self.timeout = timeout
        self.formatted_time = systime.strftime("%Y-%m-%d %H-%M-%S", systime.localtime())
        print("时间："+ self.formatted_time)
        print("网卡：", iface, "过滤器表达式：", filter, "包数量：", str(count),"超时：",timeout)
        self.init_file()

    def init_file(self):
        filename = "data/packet_record"+self.formatted_time+".txt"
        self.file = open(filename,"a")

    def record(self,p):
        record = str(p.time)+":"+p.payload.load.decode()+"\n"
        print(record)

    def sniff_scapy(self):
        self.pkts = sniff(iface=self.iface, filter=self.filter,prn=self.record,count=self.count+1,timeout=self.timeout)
        self.save_pkts()
        self.close()

    def save_pkts(self):
        print(self.pkts)
        pcap_filename = "data/pcap" + self.formatted_time + ".pcap"
        wrpcap(pcap_filename, self.pkts)
        if self.pkts:
            for pkt in self.pkts:
                record = str(pkt.time) + ":" + pkt.payload.load.decode() + "\n"
                self.file.write(record)
        else:
            print("no packet received")

    def close(self):
        self.file.close()


if __name__ == '__main__':
    # show_interfaces()
    # iface = "Intel(R) Dual Band Wireless-AC 8265"
    # iface = "Software Loopback Interface 1"
    # filter = "udp dst port 10002"
    iface = sys.argv[1]
    filter = sys.argv[2]
    count = int(sys.argv[3])
    timeout = int(sys.argv[4])
    sniff_obj = Sniff(iface,filter,count,timeout)
    sniff_obj.sniff_scapy()