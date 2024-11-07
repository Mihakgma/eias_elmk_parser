from driver import Driver
from injector import Injector
from navigator import Navigator
from singleton import Singleton


class SessionManager(Singleton):
    __SESSIONS_CREATED = []

    def __init__(self):
        self.__current_driver = None

    def start_new_session(self):
        driver = Driver()
        navigator = Navigator()
        injector = Injector(driver=driver,
                            navigator=navigator,
                            auto_charging=True)
        injector.inject()
        SessionManager.__SESSIONS_CREATED.append(navigator)

    def get_current_driver(self):
        return self.__current_driver

    def set_current_driver(self, driver):
        self.__current_driver = driver

    def stop_current_driver(self, start_new_session=False):
        self.__current_driver.discharge()
        if start_new_session:
            self.start_new_session()


if __name__ == '__main__':
    pass
