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

    # @staticmethod
    def print_running_threads(self):
        """
        Print running threads.
        """
        print("Current running threads:")
        for thread in thread_enumerate():
            print(f" - {thread.name} ({thread.ident})")
            time_sleep(self.timeout)

    # @staticmethod
    def run(self):
        lock = RLock()
        """
        Runs thread printer.
        """
        while True:
            with lock:
                lock.acquire()
                self.print_running_threads()
                lock.release()