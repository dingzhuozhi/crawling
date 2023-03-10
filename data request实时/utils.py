from datetime import datetime
from time import sleep
import pandas as pd
import socket


def send_udp(host,port,message):
    """
    :param host:
    :param port:
    :param message:
    :return:
    爬虫发送至指定端口，一般发到 127.0.0.1
    """
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.sendto(message.encode('utf-8'),(host,port))


def receive_udp(port):
    """
    :param port:
    :return: information
    """
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as udp_socket:
        local_addr = ("", port)
        udp_socket.bind(local_addr)

        recv_data = udp_socket.recvfrom(1024)
        print(recv_data[0].decode('utf-8'))
        print("发送方的ip和端口",recv_data[1])
        return recv_data[0].decode('utf-8')


log_str = ""


def log(*msgs):
    global log_str
    log_str += "=" * 100 + "\n"
    print("=" * 100)
    for msg in msgs:
        log_str += "\t" + msg + "\n"
        print("\t" + msg)
    log_str += "\t" + "当前时间：" + str(datetime.now()) + "\n"
    print("\t" + "当前时间：" + str(datetime.now()))
    log_str += "=" * 100 + "\n"
    print("=" * 100)

def get_log_str():
    global log_str
    return log_str

def dict_prettify(d, indent=0, first_indent=False):
    result = "\n".join(['\t' * indent + str(k) + '\t' + str(v) for k, v in d.items()])
    if not first_indent:
        result = result.lstrip()

    return result

def timer(date, skip=10):
    
    while datetime.now() < date:
        print(datetime.now())
        sleep(skip)
    
    
    