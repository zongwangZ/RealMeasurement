#!/usr/bin/env python
# encoding: utf-8
'''
@project : 'socket-toy'
@author  : '张宗旺'
@file    : 'client'.py
@ide     : 'PyCharm'
@time    : '2021'-'03'-'19' '15':'59':'13'
@contact : zongwang.zhang@outlook.com
'''

from socket import *
import sys
import time
import struct

# 实现各种功能请求
class TftpClient(object):
    def __init__(self, sockfd):
        super().__init__()
        self.sockfd = sockfd
        self.opt = ''

    def panel(self):
        print('+', '*'*30, '+', sep='')
        print('+', 'display'.center(30), '+', sep='')
        print('+', 'download'.center(30), '+', sep='')
        print('+', 'upload'.center(30), '+', sep='')
        print('+', 'quit'.center(30), '+', sep='')
        print('+', '*'*30, '+', sep='')

    def display(self):
        self.sockfd.send(b'display')
        print(self.sockfd.recv(1024).decode())

    def download(self):
        '客户端下载请求'
        # 先使用display命令向服务器请求文件列表，验证用户想要下载的文件是否存在
        filename = input('filename>> ')
        if not filename:
            return
        self.sockfd.send(b'display')
        files = self.sockfd.recv(1024).decode().split('\n')
        if not filename in files:
            print('Cannot locate', filename)
            return
        # 文件存在，发送下载请求到服务端，并接收返回结果
        data = 'download ' + filename
        self.sockfd.send(data.encode())
        data = self.sockfd.recv(1024).decode()
        # 如果服务端无法打开文件
        if data == 'Failed to open file':
            print('Failed to open file')
        # 可以执行下载操作
        else:
            # 调用写方法
            print(data)
            self.write(filename)
            print('Done!')

    def write(self, filename):
        '从服务器下载文件'
        # 考虑到粘包问题，导入struct模块，接收服务端要发送的数据的大小，再按照这个大小接收数据，循环执行
        fp = open(filename, 'wb')
        while True:
            # 接收数据大小，调用struct.unpack方法获得数据大小
            res = self.sockfd.recv(4)
            length = struct.unpack('i', res)[0]
            # 如果数据大小为0，说明传输结束，退出循环
            if length == 0:
                break
            # 按照数据的大小接收数据
            data = self.sockfd.recv(length)
            fp.write(data)
        fp.close()

    def upload(self):
        # 文件路径
        filepath = input('filepath>> ')
        try:
            fp = open(filepath, 'rb')
        except:
            print('Unable to open', filepath)
            return
        else:
            # 文件上传要保存为什么名字
            # 先使用display命令向服务器请求文件列表，验证用户想要上传的文件名是否存在
            filename = input('filename>> ')
            if not filename:
                return
            self.sockfd.send(b'display')
            files = self.sockfd.recv(1024).decode().split('\n')
            if filename in files:
                print('File already exists!')
                return
            # 可以上传
            data = 'upload ' + filename
            self.sockfd.send(data.encode())
            data = self.sockfd.recv(1024).decode()
            if data == 'Unable to open file':
                print('服务器打开文件出错')
                return
            else:
                self.read(fp)

    def read(self, fp):
        '读取文件上传服务器'
        while True:
            data = fp.read(1024)
            if not data:
                res = struct.pack('i', 0)
                self.sockfd.send(res)
                break
            res = struct.pack('i', len(data))
            self.sockfd.send(res)
            self.sockfd.send(data)
        print('Done!')

    def quit(self):
        self.sockfd.send(b'quit')
        self.sockfd.close()
        sys.exit('客户端关闭')

# 创建套接字，建立连接
def main():
    argc = len(sys.argv)
    if argc != 3:
        sys.exit('Usage: python client.py host port')
    else:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
        ADDR = HOST, PORT

        sockfd = socket()
        try:
            sockfd.connect(ADDR)
        except ConnectionRefusedError:
            sys.exit('无法连接到服务端')

        tftp = TftpClient(sockfd)

        tftp.panel()
        while True:
            try:
                tftp.opt = input('>> ').lower()
            except KeyboardInterrupt:
                tftp.quit()
            if tftp.opt == 'display':
                tftp.display()
            elif tftp.opt == 'download':
                tftp.download()
            elif tftp.opt == 'upload':
                tftp.upload()
            elif tftp.opt == 'quit':
                tftp.quit()
            else:
                continue


if __name__ == '__main__':
    main()