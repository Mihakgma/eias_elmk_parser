from threading import Thread, RLock
from threading import enumerate as thread_enumerate
from time import sleep as time_sleep


class ThreadsMonitor(Thread):
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
            print(f" - {thread.name} ({thread.ident})")
            time_sleep(self.timeout)

    def run(self):
        lock = RLock()
        """
        Runs thread printer.
        """
        while self.__is_running:
            with lock:
                lock.acquire()
                self.print_running_threads()
                lock.release()
        else:
            print(f"Threading of instance <{self}>\nHas been successfully stopped...")

    def close_self(self):
        self.__is_running = False

    def __str__(self):
        out = ",\n".join([
            f"\nClass name: <{self.__class__.__name__}>",
            f"Daemon: <{self.daemon}>",
            f"Set timeout: <{self.timeout}>",
            f"Is running: <{self.__is_running}>"
        ])
        return out
