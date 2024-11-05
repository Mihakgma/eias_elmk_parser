from driver import Driver
from functions import send_keys_by_xpath
from info import HOME_URL, LOGIN_XPATH, LOGIN, PASSWORD_XPATH, PASSWORD, ELMK_URL
from singleton import Singleton


class Navigator(Singleton):
    WARNINGS = {
        HOME_URL: [input, 'Confirm certificate and enter any key to continue.']
    }

    def __init__(self, browser: Driver):
        self.__browser = browser
        self.__current_url = "_"
        self.__current_application_number = -1

    def get_current_url(self):
        return self.__current_url

    def get_current_application_number(self):
        return self.__current_application_number

    def navigate(self, page_path):
        driver = self.__browser.get_driver()
        driver.get(page_path)
        warnings = self.WARNINGS
        if page_path in warnings:
            func, warn_text = warnings[page_path][0], warnings[page_path][1]
            func(warn_text)
        self.__current_url = driver.current_url

    def login(self):
        driver = self.__browser.get_driver()
        # ввод логина и пароля для входа на портал!
        send_keys_by_xpath(driver=driver,
                           xpath=LOGIN_XPATH,
                           text=LOGIN,
                           pause_secs=2.1,
                           timeout=15,
                           need_press_enter=False)

        send_keys_by_xpath(driver=driver,
                           xpath=PASSWORD_XPATH,
                           text=PASSWORD,
                           pause_secs=2.1,
                           timeout=15,
                           need_press_enter=True)
        self.__current_url = driver.current_url
        # input('Подождать пока страница прогрузится?')
        # переходим на страницу ЕЛМК
        self.navigate(ELMK_URL)
        # подождать (?) пока контент прогрузится...


if __name__ == '__main__':
    navigator = Navigator(Driver())
    print(navigator.get_current_url())
    print(navigator.get_current_application_number())
