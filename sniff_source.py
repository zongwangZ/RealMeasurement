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
    def __init__(self,iface,filter,count):
        self.iface = iface
        self.filter = filter
        self.count = count
        self.formatted_time = systime.strftime("%Y-%m-%d %H-%M-%S", systime.localtime())
        print("时间："+ self.formatted_time)
        print("网卡：", iface, "过滤器表达式：", filter, "包数量：", str(count))
        self.init_file()

    def init_file(self):
        filename = "data/packet_record"+self.formatted_time+".txt"
        self.file = open(filename,"a")

    def record(self,p):
        record = str(p.time)+":"+p.payload.load.decode()+"\n"
        print(record)
        self.file.write(record)

    def sniff_scapy(self):
        self.t = AsyncSniffer(iface=self.iface, filter=self.filter,prn=self.record,count=self.count+1,timeout=7200)
        self.t.start()
        self.t.join()
        self.save_pcap()

    def save_pcap(self):
        pkts = self.t.results
        print(pkts)
        pcap_filename = "data/pcap" + self.formatted_time + ".pcap"
        wrpcap(pcap_filename, pkts)

    def close(self):
        self.t.stop()
        self.file.close()


if __name__ == '__main__':
    # show_interfaces()
    # iface = "Intel(R) Dual Band Wireless-AC 8265"
    # iface = "Software Loopback Interface 1"
    # filter = "udp dst port 10002"
    iface = sys.argv[1]
    filter = sys.argv[2]
    count = int(sys.argv[3])
    sniff_obj = Sniff(iface,filter,count)
    sniff_obj.sniff_scapy()