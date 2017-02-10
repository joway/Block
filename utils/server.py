import os

import psutil


def server_info():
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_times()
    GB = 1024 * 1024 * 1024
    return {
        'mem_available': round(mem.available / GB, 2),
        'mem_percent': mem.percent,
        'cpu_user': cpu.user,
    }


def check_ping(host):
    response = os.system("ping -c 1 " + host)
    return response == 0
