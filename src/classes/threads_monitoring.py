from threading import Thread, RLock
from threading import enumerate as thread_enumerate
from time import sleep as time_sleep
from datetime import datetime

import psutil

from patterns.singleton import Singleton


class ThreadsMonitor(Thread, Singleton):
    def __init__(self,
                 daemon: bool = True,
                 timeout: int = 1):
        Thread.__init__(self,
                        name=self.__class__.__name__,
                        daemon=daemon)
        self.daemon = daemon
        self.timeout = timeout
        self.__is_running = True
        self.__log = {
            "ram_total": [],
            "ram_available": [],
            "ram_used": [],
            "threads_number": [],
            "time": []
        }

    def print_running_threads(self):
        """
        Print running threads.
        """
        print("Current running threads:")
        threads_number_now = 0
        ts_now = get_now_ts()
        try:
            # Get RAM info here
            memory_info = psutil.virtual_memory()
            ram_total = memory_info.total / (1024 ** 2)
            self.__log["ram_total"].append(round(ram_total, 2))
            ram_available = memory_info.available / (1024 ** 2)
            self.__log["ram_available"].append(round(ram_available, 2))
            ram_used = (memory_info.total - memory_info.available) / (1024 ** 2)
            self.__log["ram_used"].append(round(ram_used, 2))
        except Exception as e:
            print(f"Error getting RAM information: {e}")
        for thread in thread_enumerate():
            threads_number_now += 1
            try:
                print(f" - {thread.name} ({thread.ident})")
            except Exception as e:
                print(f" Error getting info of: {thread.name}: {e}")
        self.__log["threads_number"].append(threads_number_now)
        self.__log["time"].append(ts_now)
        print(f"Current RAM total: {ram_used:.2f} MB")

    def run(self):
        lock = RLock()
        """
        Runs thread printer.
        """
        while self.__is_running:
            time_sleep(self.timeout)
            with lock:
                lock.acquire()
                self.print_running_threads()
                lock.release()
        else:
            print(f"Threading of instance <{self}>\nHas been successfully stopped...")

    def stop(self):
        self.__is_running = False

    def get_log(self):
        return self.__log

    def __str__(self):
        out = ",\n".join([
            f"\nClass name: <{self.__class__.__name__}>",
            f"Daemon: <{self.daemon}>",
            f"Set timeout: <{self.timeout}>",
            f"Is running: <{self.__is_running}>"
        ])
        return out


def get_now_ts():
    dt = datetime.now()
    timeStamp = dt.strftime('%Y-%m-%d %H:%M:%S')
    return timeStamp


if __name__ == '__main__':
    threads_monitor = ThreadsMonitor()
    threads_monitor.start()
    time_sleep(5)
    threads_monitor.stop()
    log = threads_monitor.get_log()
    print(*[(k, v) for (k, v) in log.items()], sep="\n")
