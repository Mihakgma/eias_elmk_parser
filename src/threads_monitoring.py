from threading import Thread
from threading import enumerate as thread_enumerate
from time import sleep as time_sleep


class ThreadsMonitor:
    def __init__(self,
                 daemon: bool = True,
                 timeout: int = 10,):
        # Thread.__init__(self, name=self.__class__.__name__)
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

    @staticmethod
    def run(self):
        """
        Runs thread printer.
        """
        thread = Thread(target=self.print_running_threads, daemon=self.daemon)
        thread.start()
