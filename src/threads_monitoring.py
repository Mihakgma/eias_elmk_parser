from threading import Thread
from threading import enumerate as thread_enumerate
from time import sleep as time_sleep


class ThreadsMonitor(Thread):
    def __init__(self,
                 daemon: bool = True,
                 timeout: int = 10,):
        Thread.__init__(self)
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

    def run_thread_printer(self):
        """
        Runs thread printer.
        """
        thread = Thread(target=self.print_running_threads, daemon=self.daemon)
        thread.start()
