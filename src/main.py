from patterns.funct_wrapper import handle_exceptions_quit_driver
from classes.session_manager import SessionManager
from classes.threads_monitoring import ThreadsMonitor


class ELMKParser:

    @staticmethod
    @handle_exceptions_quit_driver
    def start(test_regime: bool = False,
              ask_for_cancel_interval_navigator=5000,
              sleep_secs_up_to_navigator=1.1,
              sleep_secs_up_to_pesr_data_navigator=0.5,
              daemon_tm: bool=False):

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
            navigator(ask_for_cancel_interval=ask_for_cancel_interval_navigator,
                      sleep_secs_up_to=sleep_secs_up_to_navigator,
                      sleep_secs_up_to_pesr_data=sleep_secs_up_to_pesr_data_navigator)
            threads_monitoring = ThreadsMonitor(daemon=daemon_tm)
            threads_monitoring.start()


if __name__ == '__main__':
    ELMKParser().start(test_regime=True)
