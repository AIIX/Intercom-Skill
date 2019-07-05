#!/usr/bin/env python
import socket
from multiprocessing import Process, Queue
import time
import argparse

def check_server(address, port, queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((address, port))
        queue.put((True, address, port))
    except (KeyboardInterrupt, OSError, socket.error) as e:
        queue.put_nowait((False, address, port))
    #except socket.error as e:

def get_own_ip():
    return ((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])


def check_subnet_for_open_port(subnet, port, timeout=3.0):
    q = Queue()
    processes = []
    for i in range(1, 255):
        ip = subnet + '.' + str(i)
        p = Process(target=check_server, args=[ip, port, q])
        processes.append(p)
        p.start()
    time.sleep(timeout)

    found_ips = []
    for idx, p in enumerate(processes):
        if p.exitcode is None:
            p.terminate()
        else:
            open_ip, address, port = q.get()
            if open_ip:
                found_ips.append(address)
            p.terminate()

    return found_ips

def discover_device_name(iplist):
    deviceList = []
    deviceListObj = {}
    deviceList.clear()
    for address in iplist:
        if address:
            sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sd.connect((address, 50000))
            device_name = sd.recv(1024)
            sd.close()
            dname =  device_name.decode("utf-8")
            device = {"address": address, "devicename": dname}
            deviceList.append(device)
            deviceListObj["Devices"] = deviceList
    return deviceListObj
        
def check_own_subnet_for_open_port(port, timeout=3.0):
    own_ip = get_own_ip()
    ip_split = own_ip.split('.')
    subnet = ip_split[:-1]
    subnetstr = '.'.join(subnet)
    return check_subnet_for_open_port(subnetstr, port)
