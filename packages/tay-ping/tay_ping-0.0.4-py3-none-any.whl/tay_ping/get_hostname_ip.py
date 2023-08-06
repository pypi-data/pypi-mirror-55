#!/usr/bin/env python
# -*- coding:utf-8 -*-


import socket


def get_ip(this_hostname):
    """
    根据主机名获取对应的IP地址
    :param this_hostname: 填写一个主机名
    :return: 返回一个String
    """
    try:
        # 如果ping不通代表主机名解析还没有生效或者机器不存在
        ip = socket.gethostbyname(this_hostname)
        return "{:-<20} {}".format(ip, this_hostname)

    except:
        return "{} 无法Ping通。。。".format(this_hostname)


def get_print():
    print("123")


if __name__ == "__main__":
    print(get_ip(this_hostname="clSvcProcore19"))
