#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-23 00:06:43
# @Description : 向远程服务器发送unique_id
"""


import socket


def UNIQUE_ID_send(unique_id: str) -> bool:
    """
    向远程服务器发送unique_id
    
    args:
        unique_id (str): TikTok中用户的唯一ID
    
    returns:
        True: 如果服务器返回的值与unique_id相同, 则证明服务器接收到了值
        False: 服务器接收数据异常/发送异常
    """
    host = '8.130.37.144'
    port = 8888

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    client.send(unique_id.encode())

    response = client.recv(4096)

    check = response.decode('UTF-8')
    if unique_id == check:
        return True
    return False

if __name__ == '__main__':
    UNIQUE_ID_send(unique_id='moker')