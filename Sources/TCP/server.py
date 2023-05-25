#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Moker
# @Created Time : 2023-05-23 00:10:02
# @Description :
"""


import socket
import threading
from time import sleep

# 定义共享变量
result = None

def handle_client(client_socket):
    global result

    request = client_socket.recv(1024)
    check = request.decode('UTF-8')
    result = check
    print(f'result: {result}')
    result = None

    client_socket.send(check.encode())
    client_socket.close()

def server():
    bind_ip = '0.0.0.0'
    bind_port = 8888

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen()

    print(f'[*] Listening on {bind_ip}:{bind_port}')

    while True:
        client, addr = server.accept()

        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

        print(f'result: {result}')

def print_result():
    while True:
        print(f'result: {result}')
        sleep(1)


if __name__ == '__main__':
    server_handler = threading.Thread(target=server, args=())
    print_result_handler = threading.Thread(target=print_result, args=())

    server_handler.start()
    print_result_handler.start()

    server_handler.join()
    print_result_handler.join()