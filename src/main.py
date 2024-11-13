# from threading import Thread

from session_manager import SessionManager
from text_caching import TextCaching

# from threading import Thread

from threads_monitoring import ThreadsMonitor


class ELMKParser:

    @staticmethod
    def start(test_regime: bool = False,
              text_caching_sleep=3,
              ask_for_cancel_interval_navigator=5000,
              sleep_secs_up_to_navigator=1.1,
              sleep_secs_up_to_pesr_data_navigator=0.5,
              max_iterations_caching=15,
              cache_dir_caching="..\\text_data"):

        session_manager = SessionManager()
        session_manager.start_new_session()
        navigator = session_manager.get_navigator()
        driver = navigator.get_driver()
        driver_s_m = session_manager.get_current_driver()
        print("\nDrivers from navigator & session_manager are equal?")
        print(driver == driver_s_m)
        if test_regime:
            return
        else:
            text_caching = TextCaching(sleep_time=text_caching_sleep,
                                       obj=navigator,
                                       cache_dir=cache_dir_caching,
                                       max_iterations=max_iterations_caching)
            threads_monitoring = ThreadsMonitor()

            threads_to_start = {
                navigator: [
                    ask_for_cancel_interval_navigator,
                    sleep_secs_up_to_navigator,
                    sleep_secs_up_to_pesr_data_navigator
                ],
                text_caching: [],
                threads_monitoring: [],
            }

            threads_to_join = []
            for (t, p) in threads_to_start.items():
                # thread = Thread(target=t, args=p)
                threads_to_join.append(t)
                t.start()

            for thread in threads_to_join:
                thread.join()


if __name__ == '__main__':
    ELMKParser().start(test_regime=False)
