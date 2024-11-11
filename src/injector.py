from driver import Driver
from navigator import Navigator
# from session_manager import SessionManager


class Injector:
    def __init__(self,
                 driver: Driver,
                 navigator: Navigator,
                 session_manager,
                 auto_charging: bool = True):
        self.__driver = driver
        self.__navigator = navigator
        self.__session_manager = session_manager
        self.__auto_charging = auto_charging

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, value: Driver):
        if not isinstance(value, Driver):
            raise TypeError("driver must be of type Driver")
        self.__navigator = value

    @property
    def navigator(self):
        return self.__navigator

    @navigator.setter
    def navigator(self, value: Navigator):
        if not isinstance(value, Navigator):
            raise TypeError("navigator must be of type Navigator")
        self.__navigator = value

    @property
    def auto_charging(self):
        return self.__auto_charging

    @auto_charging.setter
    def auto_charging(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("auto_charging must be of type bool")
        self.__auto_charging = value

    def inject(self):
        driver = self.__driver
        navigator = self.__navigator
        session_manager = self.__session_manager
        auto_charging = self.__auto_charging
        if auto_charging:
            driver.charge()
        navigator.set_driver(driver)
        session_manager.set_current_driver(driver)
