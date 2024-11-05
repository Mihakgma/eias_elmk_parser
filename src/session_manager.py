from driver import Driver
from singleton import Singleton


class SessionManager(Singleton):
    __SESSIONS_CREATED = []

    def __init__(self):
        self.__current_session = None

    def start_new_session(self):
        driver = Driver()
        driver.charge()
        self.__current_session = driver
        SessionManager.__SESSIONS_CREATED.append(driver)

    def get_current_session(self):
        return self.__current_session

    def stop_current_session(self, start_new_session=False):
        self.__current_session.discharge()
        if start_new_session:
            self.start_new_session()


if __name__ == '__main__':
    pass
