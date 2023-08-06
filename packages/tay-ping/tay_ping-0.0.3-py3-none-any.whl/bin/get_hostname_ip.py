#!/usr/bin/env python
# -*- coding:utf-8 -*-


import socket


def get_ip(this_hostname):
    """
    根据主机名获取对应的IP地址
    :param this_hostname: 填写一个主机名
    :return: 没有返回值，只是在控制台打印信息
    """
    try:
        # 如果ping不通代表主机名解析还没有生效或者机器不存在
        ip = socket.gethostbyname(this_hostname)
        print("{} {}".format(ip, this_hostname))
    except:
        print("{} 无法Ping通。。。".format(this_hostname))
