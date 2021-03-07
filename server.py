#!/usr/bin/env python
# encoding: utf-8
'''
@project : 'RealMeasurement'
@author  : '张宗旺'
@file    : 'server'.py
@ide     : 'PyCharm'
@time    : '2021'-'03'-'02' '15':'48':'47'
@contact : zongwang.zhang@outlook.com
'''
import socket
import sys
import time

class ProbeServer:
    def __init__(self, addr:tuple):
        self.addr = addr
        self.__init_socket()

    def __init_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(self.addr)

    def run(self):
        while True:
            data, addr = self.s.recvfrom(2048)
            print("at:",time.time(),"received:", data.decode(), "from", addr)
            if data.decode() == "end1":
                break
        self.s.close()


if __name__ == '__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])
    print("ip："+ip)
    print("port："+str(port))
    addr = (ip,port)
    server = ProbeServer(addr)
    # server.run()