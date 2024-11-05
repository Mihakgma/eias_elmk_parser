from driver import Driver
from functions import send_keys_by_xpath
from info import HOME_URL, LOGIN_XPATH, LOGIN, PASSWORD_XPATH, PASSWORD, ELMK_URL
from singleton import Singleton


class Navigator(Singleton):

    WARNINGS = {
        HOME_URL: [input, 'Confirm certificate and enter any key to continue.']
    }

    def __init__(self, browser: Driver):
        self.browser = browser
        self.current_url = ""

    def navigate(self, page_path):
        driver = self.browser.get_driver()
        driver.get(page_path)
        warnings = self.WARNINGS
        if page_path in warnings:
            func, warn_text = warnings[page_path][0], warnings[page_path][1]
            func(warn_text)
        self.current_url = driver.current_url

    def login(self):
        driver = self.browser.get_driver()
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
        self.current_url = driver.current_url
        # input('Подождать пока страница прогрузится?')
        # переходим на страницу ЕЛМК
        self.navigate(ELMK_URL)
        # подождать (?) пока контент прогрузится...


if __name__ == '__main__':
    pass
