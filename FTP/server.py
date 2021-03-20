#!/usr/bin/env python
# encoding: utf-8
'''
@project : 'socket-toy'
@author  : '张宗旺'
@file    : 'server.py'.py
@ide     : 'PyCharm'
@time    : '2021'-'03'-'19' '15':'58':'36'
@contact : zongwang.zhang@outlook.com
'''
import struct
from socket import *
import os
import signal
import sys
import time

# 文件库
FILE_PATH = 'D:/ftp_receive/'

# 实现功能模块
class TftpServer(object):
    def __init__(self, sockfd, addr):
        super().__init__()
        self.sockfd = sockfd
        self.addr = addr
        self.opt = ''

    def display(self):
        re = ''
        for i in os.listdir(FILE_PATH):
            re += i + '\n'
        self.sockfd.send(re.encode())

    def download(self):
        '下载模块功能实现'
        # 尝试打开文件
        filename = FILE_PATH + self.opt.split(' ')[1]
        print(filename)
        try:
            fp = open(filename, 'rb')
        except:
            self.sockfd.send(b'Failed to open file')
        else:
            self.sockfd.send(b'Ready to transfer')
            # 循环发送数据
            while True:
                data = fp.read(1024)
                if not data:
                    # 如果传输完毕，data为空，传输0，跳出循环
                    res = struct.pack('i', 0)
                    self.sockfd.send(res)
                    break
                res = struct.pack('i', len(data))
                self.sockfd.send(res)
                self.sockfd.send(data)
            print('Done!')

    def upload(self):
        filename = FILE_PATH + self.opt.split(' ')[1]
        try:
            fp = open(filename, 'wb')
        except:
            self.sockfd.send('Unable to open file'.encode())
        else:
            self.sockfd.send(b'Ready to upload')
            while True:
                res = self.sockfd.recv(4)
                length = struct.unpack('i', res)[0]
                if length == 0:
                    break
                data = self.sockfd.recv(length)
                fp.write(data)
            fp.close()
            print('Done!')


    def quit(self):
        print(self.addr, '断开连接')
        self.sockfd.close()
        sys.exit()

# 主流程
def main():
    HOST = '172.27.90.37'
    PORT = 5555
    ADDR = (HOST, PORT)

    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    # 通知内核对子进程的结束不关心,由内核回收。
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        print('连接成功：', addr)

        # 创建子进程
        pid = os.fork()

        if pid == 0:
            sockfd.close()
            tftp = TftpServer(connfd, addr)
            while True:
                tftp.opt = connfd.recv(1024).decode()
                if tftp.opt == 'display':
                    tftp.display()
                elif tftp.opt.startswith('download'):
                    tftp.download()
                elif tftp.opt.startswith('upload'):
                    tftp.upload()
                elif tftp.opt == 'quit':
                    tftp.quit()
        else:
            connfd.close()
            continue


if __name__ == '__main__':
    main()