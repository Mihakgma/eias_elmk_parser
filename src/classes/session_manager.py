from classes.driver import Driver
from classes.inject_manager import InjectManager
from classes.navigator import Navigator
from patterns.singleton import Singleton
# from deprecated.text_caching import TextCaching


class SessionManager(Singleton):
    """
    need to think if I need to add field
    navigator = Navigator() ???
    """
    __SESSIONS_CREATED = []

    def __init__(self):
        self.__current_driver = None
        self.__current_navigator = None

    @staticmethod
    def get_sessions_created():
        return SessionManager.__SESSIONS_CREATED

    @staticmethod
    def clear_previous_sessions():
        sessions_saved = SessionManager.__SESSIONS_CREATED
        if len(sessions_saved) > 1:
            for navigator, i in zip(sessions_saved, range(len(sessions_saved))):
                if i < (len(sessions_saved) - 1):
                    d = navigator.get_driver_obj()
                    print(f"Deleting data for navigator with driver ID = <{d}>")
                    navigator.clear_memory(all_data=True)
        else:
            pass

    def start_new_session(self, test_regime: bool=False):
        my_driver = Driver()
        self.__current_driver = my_driver
        my_navigator = Navigator()
        self.__current_navigator = my_navigator
        InjectManager.do_inject(driver=my_driver,
                                navigator=my_navigator,
                                session_manager=self,
                                auto_charge=True)
        SessionManager.__SESSIONS_CREATED.append(my_navigator)
        if not test_regime:
            my_navigator()

    def get_current_driver(self):
        return self.__current_driver

    def set_current_driver(self, driver):
        self.__current_driver = driver

    def get_navigator(self):
        return self.__current_navigator

    def stop_current_session(self,
                             start_session_automatically=False,
                             clear_previous_navigators: bool = False,
                             test_regime: bool=False):
        """
        Для данного метода необходимо продумать,
        как очищать память по сохраненным объектам навигатор, а именно,
        в плане очистки данных в них с помощью метода clear_memory(),
        предположительно необходимо будет очищать ВСЕ данные у объектов этого класса
        ЗА ИСКЛЮЧЕНИЕМ ПОСЛЕДНЕГО ОБЪЕКТА КЛАССА НАВИГАТОР,
        ПОМЕЩЕННЫХ (СОЗДАННЫХ РАНЕЕ) В ПОЛЕ ТЕКУЩЕГО КЛАССА __SESSIONS_CREATED!!!


        DONE !!! NEED TO CHECK!!!
        :param start_session_automatically:
        :return:
        """
        self.__current_driver.discharge()
        if clear_previous_navigators:
            SessionManager.clear_previous_sessions()
        if start_session_automatically:
            self.start_new_session(test_regime=test_regime)


if __name__ == '__main__':
    text_caching_sleep = 3
    ask_for_cancel_interval_navigator = 5000
    sleep_secs_up_to_navigator = 1.1
    sleep_secs_up_to_pesr_data_navigator = 0.5

    session_manager = SessionManager()
    session_manager.start_new_session(test_regime=True)
    session_manager.stop_current_session(start_session_automatically=True,
                                         clear_previous_navigators=False,
                                         test_regime=True)
    session_manager.stop_current_session(start_session_automatically=True,
                                         clear_previous_navigators=True,
                                         test_regime=True)
    session_manager.stop_current_session(start_session_automatically=False,
                                         clear_previous_navigators=True,
                                         test_regime=True)
    sessions = SessionManager().get_sessions_created()
    for n in sessions:
        print(n)
        d = n.get_driver_obj()
        print(d)
