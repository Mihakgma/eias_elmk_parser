from classes.driver import Driver
from classes.inject_manager import InjectManager
from classes.navigator import Navigator
from patterns.singleton import Singleton

from time import sleep as time_sleep
from os import path as os_path
from os import makedirs as os_makedirs
import json

from patterns.thread_func import thread
from data import APPLICATIONS_NUMBERS_COUNTER_FILE, LOGS_DIR


class SessionManager(Singleton):
    """
    manages sessions (Navigator class),
    realizes adapter pattern to inject driver to navigator and navigator
    to session manager instance...
    """
    __SESSIONS_CREATED = []

    def __init__(self):
        self.__current_driver = None
        self.__current_navigator = None
        self.__start_session_automatically = False

    def set_start_session_automatically(self, start_session_automatically):
        self.__start_session_automatically = start_session_automatically

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

    def start_new_session(self,
                          test_regime: bool = False,
                          personal_data_by_filter=True,
                          need_parse_left_df=False,
                          *args,
                          **kwargs):
        my_driver = Driver()
        self.__current_driver = my_driver
        my_navigator = Navigator()
        my_navigator.set_personal_data_by_filter(personal_data_by_filter)
        my_navigator.set_need_parse_left_df(need_parse_left_df=need_parse_left_df)
        self.__current_navigator = my_navigator
        InjectManager.do_inject(driver=my_driver,
                                navigator=my_navigator,
                                session_manager=self,
                                auto_charge=True)
        SessionManager.__SESSIONS_CREATED.append(my_navigator)
        if not test_regime:
            observe_session(session_manager=self, navigator=my_navigator, driver=my_driver)
            my_navigator.deserialize()
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
                             test_regime: bool = False):
        """
        this method will stop the current session
        :param start_session_automatically:
        :param clear_previous_navigators: - delete navigators after start session
        :param test_regime: no comments...
        :return:
        """
        self.__current_driver.discharge()
        self.__current_navigator.serialize()
        if clear_previous_navigators:
            SessionManager.clear_previous_sessions()
        if self.__start_session_automatically:
            self.start_new_session(test_regime=test_regime)


@thread
def observe_session(session_manager: SessionManager,
                    navigator: Navigator,
                    driver: Driver,
                    check_time_seconds: int = 60,
                    max_iter_per_application: int = 5,
                    start_session_automatically=True,
                    clear_previous_navigators: bool = True,
                    test_regime: bool = False):
    application_skipped: bool = False
    checks_per_application = {
        "driver_id": driver.get_id(),
        "navigator": str(navigator),
        "check_time_seconds": check_time_seconds,
        "max_iter_per_application": max_iter_per_application,
        "start_session_automatically": start_session_automatically,
        "clear_previous_navigators": clear_previous_navigators,
        "test_regime": test_regime}
    try:
        while driver.is_charged():
            time_sleep(check_time_seconds)
            application_number = navigator.get_current_application_number()
            if application_number == -1:
                pass
            elif application_number in checks_per_application:
                checks_per_application[application_number] += 1
                if checks_per_application[application_number] > max_iter_per_application:
                    navigator.set_appl_numbers(navigator.get_appl_numbers()[1:])
                    application_skipped = True
                    session_manager.stop_current_session(start_session_automatically=start_session_automatically,
                                                         clear_previous_navigators=clear_previous_navigators,
                                                         test_regime=test_regime)
            else:
                print(f"for application number <{application_number}>")
                print(f"has been done <{checks_per_application[application_number]}> tries"
                      f"of possible <{max_iter_per_application}> iterations...")
                checks_per_application[application_number] = 1
        else:
            print("trying to save application numbers tries")
            try:  # Handle potential errors during serialization
                fullpath_json = os_path.join(LOGS_DIR, APPLICATIONS_NUMBERS_COUNTER_FILE)
                os_makedirs(LOGS_DIR, exist_ok=True)
                with open(fullpath_json, "w", encoding='utf-8') as f:  # Добавлено encoding='utf-8'
                    json.dump(checks_per_application, f, indent=4)  # Используем json.dump, а не f.write
                print(f"Application numbers of tries has been successfully to <{APPLICATIONS_NUMBERS_COUNTER_FILE}>")
            except Exception as e:
                print(f"Error during saving application numbers of tries: {e}")

    except Exception as e:
        try:  # Handle potential errors during serialization
            fullpath_json = os_path.join(LOGS_DIR, APPLICATIONS_NUMBERS_COUNTER_FILE)
            os_makedirs(LOGS_DIR, exist_ok=True)
            with open(fullpath_json, "w", encoding='utf-8') as f:  # Добавлено encoding='utf-8'
                json.dump(checks_per_application, f, indent=4)  # Используем json.dump, а не f.write
            print(f"Application numbers of tries has been successfully to <{APPLICATIONS_NUMBERS_COUNTER_FILE}>")
        except Exception as e:
            print(f"Error during saving application numbers of tries: {e}")
        if not application_skipped:
            navigator.set_appl_numbers(navigator.get_appl_numbers()[1:])
        session_manager.stop_current_session(start_session_automatically=start_session_automatically,
                                             clear_previous_navigators=clear_previous_navigators,
                                             test_regime=test_regime)


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
