from driver import Driver
from inject_manager import InjectManager
# from injector import Injector
from navigator import Navigator
from singleton import Singleton
from text_caching import TextCaching


class SessionManager(Singleton):
    """
    need to think if I need to add field
    navigator = Navigator() ???
    """
    __SESSIONS_CREATED = []

    def __init__(self):
        self.__current_driver = None
        self.__current_navigator = None

    def start_new_session(self):
        my_driver = Driver()
        self.__current_driver = my_driver
        my_navigator = Navigator()
        self.__current_navigator = my_navigator
        InjectManager.do_inject(driver=my_driver,
                                navigator=my_navigator,
                                session_manager=self,
                                auto_charge=True)
        SessionManager.__SESSIONS_CREATED.append(my_navigator)

    def get_current_driver(self):
        return self.__current_driver

    def set_current_driver(self, driver):
        self.__current_driver = driver

    def get_navigator(self):
        return self.__current_navigator

    def stop_current_session(self,
                             start_session_automatically=False):
        self.__current_driver.discharge()
        if start_session_automatically:
            self.start_new_session()


if __name__ == '__main__':
    text_caching_sleep = 3
    ask_for_cancel_interval_navigator = 5000
    sleep_secs_up_to_navigator = 1.1
    sleep_secs_up_to_pesr_data_navigator = 0.5

    session_manager = SessionManager()
    session_manager.start_new_session()
    navigator = session_manager.get_navigator()
    text_caching = TextCaching(sleep_time=text_caching_sleep,
                               obj=navigator)
    text_caching.start()
    navigator(ask_for_cancel_interval=ask_for_cancel_interval_navigator,
              sleep_secs_up_to=sleep_secs_up_to_navigator,
              sleep_secs_up_to_pesr_data=sleep_secs_up_to_pesr_data_navigator)
