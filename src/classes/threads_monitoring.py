from threading import Thread, RLock
from threading import enumerate as thread_enumerate
from time import sleep as time_sleep

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

    def print_running_threads(self):
        """
        Print running threads.
        """
        print("Current running threads:")
        for thread in thread_enumerate():
            try:
                process = psutil.Process(thread.ident)
                memory_info = process.memory_info()
                memory_usage = memory_info.rss / (1024 ** 2)  # Memory in MB
                print(f" - {thread.name} ({thread.ident}) - Memory usage: {memory_usage:.2f} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                print(f" - {thread.name} ({thread.ident}) - {type(e).__name__}: {e}")
            except Exception as e:
                print(f" - Error getting memory usage for {thread.name}: {e}")
            # time_sleep(self.timeout)

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

    def __str__(self):
        out = ",\n".join([
            f"\nClass name: <{self.__class__.__name__}>",
            f"Daemon: <{self.daemon}>",
            f"Set timeout: <{self.timeout}>",
            f"Is running: <{self.__is_running}>"
        ])
        return out


if __name__ == '__main__':
    threads_monitor = ThreadsMonitor()
    threads_monitor.start()
    time_sleep(5)
    threads_monitor.stop()
