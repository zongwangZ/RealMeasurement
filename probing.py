#!/usr/bin/env python
# encoding: utf-8
'''
@project : 'socket-toy'
@author  : '张宗旺'
@file    : 'B2BProbe'.py
@ide     : 'PyCharm'
@time    : '2021'-'03'-'02' '10':'56':'19'
@contact : zongwang.zhang@outlook.com
'''

"""
back to back probing
背靠背探测
"""
import socket
import time
import sys
from threading import Timer
class B2BProbing:
    def __init__(self, addr1:tuple, addr2:tuple, addr3:tuple, nums:int=1000, probe_interval:int=10, packet_interval:int=0):
        self.addr1 = addr1
        self.addr2 = addr2
        self.addr3 = addr3
        print("目的地址1为：",str(addr1))
        print("目的地址2为：",str(addr2))
        print("目的地址3为：",str(addr3))
        print("发包数量为：",str(nums))
        self.nums = nums
        self.probe_interval = probe_interval  # 单位为ms
        self.packet_interval = packet_interval  # 单位ms
        self.__init_socket()


    def __init_socket(self):
        self.s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s3 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def send_probe(self, id):
        payload1 = "s1:" + str(id)
        payload2 = "s2:" + str(id)
        payload3 = "s3:" + str(id)
        self.s1.sendto(payload1.encode("utf-8"), self.addr1)
        self.s2.sendto(payload2.encode("utf-8"), self.addr2)
        self.s3.sendto(payload3.encode("utf-8"), self.addr3)

    def probing(self):
        id = 0
        while id < self.nums:
            self.send_probe(id)
            time.sleep(self.probe_interval/1000)
            id += 1

        # 结束探测
        self.s1.sendto("end".encode(), self.addr1)
        self.s2.sendto("end".encode(), self.addr2)
        self.s3.sendto("end".encode(), self.addr3)

    def close(self):
        self.s1.close()
        self.s2.close()
        self.s3.close()



if __name__ == '__main__':
    addr1 = ("1.15.81.154",10002)
    addr2 = ("82.156.15.153",10003)
    addr3 = ("120.24.37.43",10004)

    # addr1 = ("127.0.0.1",10002)
    # addr2 = ("127.0.0.1",10003)
    # addr3 = ("127.0.0.1",10004)

    nums = int(sys.argv[1])
    probing = B2BProbing(addr1,addr2,addr3,nums)
    probing.probing()
    probing.close()
