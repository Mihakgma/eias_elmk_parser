from patterns.funct_wrapper import handle_exceptions_quit_driver
from classes.session_manager import SessionManager
from classes.threads_monitoring import ThreadsMonitor


class ELMKParser:

    @staticmethod
    @handle_exceptions_quit_driver
    def start(test_regime: bool = False,
              text_caching_sleep=3,
              ask_for_cancel_interval_navigator=5000,
              sleep_secs_up_to_navigator=1.1,
              sleep_secs_up_to_pesr_data_navigator=0.5,
              max_iterations_caching=5,
              data_dir_caching="..\\text_data"):

        session_manager = SessionManager()
        session_manager.start_new_session()
        navigator = session_manager.get_navigator()
        driver = navigator.get_driver_obj()
        driver_s_m = session_manager.get_current_driver()
        print("\nDrivers from navigator & session_manager are equal?")
        print(driver == driver_s_m)
        if test_regime:
            return
        else:
            threads_monitoring = ThreadsMonitor()
            threads_monitoring.start(ask_for_cancel_interval_navigator,
                                     sleep_secs_up_to_navigator,
                                     sleep_secs_up_to_pesr_data_navigator)


if __name__ == '__main__':
    ELMKParser().start(test_regime=True)
