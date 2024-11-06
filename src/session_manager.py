from driver import Driver
from navigator import Navigator
from singleton import Singleton


class SessionManager(Singleton):
    __SESSIONS_CREATED = []

    def __init__(self):
        self.__current_driver = None

    def start_new_session(self):
        driver = Driver()
        driver.charge()
        navigator = Navigator(driver)
        self.__current_driver = driver
        SessionManager.__SESSIONS_CREATED.append(navigator)

    def get_current_driver(self):
        return self.__current_driver

    def stop_current_driver(self, start_new_session=False):
        self.__current_driver.discharge()
        if start_new_session:
            self.start_new_session()


if __name__ == '__main__':
    pass
