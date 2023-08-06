import psutil
import multiprocessing
from time import time, sleep
from threaders import threaders
from datetime import datetime, timedelta
from qaviton_monitors.log import monitor_logger


class bitsize:
    by = 2*3
    kb = 2**10
    mb = 2**20
    gb = 2**30


def net_io():
    return psutil.net_io_counters().bytes_recv, psutil.net_io_counters().bytes_sent


class NetBan:
    def __init__(self):
        i1, o1 = net_io()
        i2, o2 = net_io()
        self.bytes_recv = (i1, i2)
        self.bytes_sent = (o1, o2)
        self.timedelta = (time(), time())

    def convert(self, measurement):
        return round((measurement[1] - measurement[0]) * bitsize.by / bitsize.gb / (self.timedelta[1] - self.timedelta[0]), 3)

    def measure(self, bytes_recv, bytes_sent):
        self.timedelta = (self.timedelta[1], time())
        self.bytes_recv = (self.bytes_recv[1], bytes_recv)
        self.bytes_sent = (self.bytes_sent[1], bytes_sent)

    def GBs(self, bytes_recv, bytes_sent):
        self.measure(bytes_recv, bytes_sent)
        return f'NetIO {self.convert(self.bytes_recv)}:{self.convert(self.bytes_sent)} GBs'


def system_stats():
    boot_time = psutil.boot_time()
    return {
        "memory": psutil.virtual_memory().percent,
        "cpu": psutil.cpu_percent(),
        "disk": psutil.disk_usage("/").percent,
        "pids": len(psutil.pids()),
        "boot_time": boot_time,
        "uptime": time() - boot_time,
    }


def system_stats_raw():
    boot_time = psutil.boot_time()
    return {
        "memory": psutil.virtual_memory(),
        "cpu": psutil.cpu_percent(),
        "disk": psutil.disk_usage("/"),
        "pids": len(psutil.pids()),
        "boot_time": datetime.fromtimestamp(boot_time),
        "uptime": time() - boot_time,
        "net": net_io()
    }


def bytes_to_GB(bytes):
    return round(bytes/bitsize.gb, 3)


def monitor(delay:float=2.0):
    def get_stats():
        """:rtype: threaders.Thread"""
        stats = system_stats_raw()
        log.info(
            f"CPU {stats['cpu']}%  "
            f"MEMORY {stats['memory'].percent}%  "
            f"DISK {stats['disk'].percent}%  "
            f"Running Processes {stats['pids']}  "
            f"{net.GBs(*stats['net'])}"
        )

    @threaders.threader()
    def quit():
        """:rtype: threaders.Thread"""
        input('\n         Press Enter to stop monitoring\n\n')


    print("======================== Monitor ========================")
    stats = system_stats_raw()
    net = NetBan()

    print(f"Last Boot: {stats['boot_time']}")
    print(f"System Uptime: {timedelta(seconds=stats['uptime'])}\n")

    print(f"CPU Cores {multiprocessing.cpu_count()}")
    print(
        f"MEMORY"
        f" total {bytes_to_GB(stats['memory'].total)}GB "
        f"| used {bytes_to_GB(stats['memory'].used)}GB "
        f"| free {bytes_to_GB(stats['memory'].free)}GB "
    )
    print(
        f"DISK"
        f" total {bytes_to_GB(stats['disk'].total)}GB "
        f"| used {bytes_to_GB(stats['disk'].used)}GB "
        f"| free {bytes_to_GB(stats['disk'].free)}GB "
    )

    stop_thread = quit()
    sleep(delay)
    log = monitor_logger()

    while stop_thread.is_alive():
        get_stats()
        sleep(delay)

    stop_thread.join()
