from selenium import webdriver

from selenium.common.exceptions import WebDriverException

from data import BROWSER_FILE_PATH, WEBDRIVER_PATH, DRIVER_ARGUMENTS, START_KEY_WORD


class Driver:
    __BROWSER_FILE_PATH: str = BROWSER_FILE_PATH
    __WEBDRIVER_PATH: str = WEBDRIVER_PATH
    __DRIVER_ARGUMENTS: list = DRIVER_ARGUMENTS
    __DRIVERS_CREATED: int = 0
    __START_KEY_WORD: str = START_KEY_WORD
    CURRENT_INSTANCE = None

    def __new__(cls, *args, **kwargs):
        cls.__DRIVERS_CREATED += 1
        cls.CURRENT_INSTANCE = super(Driver, cls).__new__(cls)
        return cls.CURRENT_INSTANCE

    def __init__(self,
                 wait_secs: int = 10):
        self.__wait_secs = wait_secs
        self.__charged = False
        self.__driver = None
        self.__ID = Driver.__DRIVERS_CREATED
        self.__linked_navigator = None

    def get_linked_navigator(self):
        return self.__linked_navigator

    def set_linked_navigator(self, linked_navigator):
        self.__linked_navigator = linked_navigator

    def charge(self, test=True):
        # self.start()  # start new thread
        if test:
            self.__charged = True
        print(f"Driver number: <{self.__DRIVERS_CREATED}> has been initiated.")
        options = webdriver.ChromeOptions()
        ###
        for args in DRIVER_ARGUMENTS:
            options.add_argument(args)
        ###
        options.binary_location = self.__BROWSER_FILE_PATH
        try:
            self.__driver = webdriver.Chrome(executable_path=self.__WEBDRIVER_PATH,
                                             options=options)
            self.__driver.implicitly_wait(self.__wait_secs)
            self.__charged = True
        except TypeError as e:
            print(e)
            print("Selenium driver error: probably versions conflict...")
        except WebDriverException as wde:
            print(wde)
            print(f"Cannon find text <{self.__START_KEY_WORD}>!!!")

    def discharge(self):
        if self.__charged:
            try:
                self.__charged = False
                self.__driver.quit()
                print('Selenium driver has been successfully closed.')
            except BaseException as e:
                print('An exception occurred while Selenium driver discharging.')
                print(e)
        else:
            print("Cannot discharge driver: Driver has not been charged yet.")

    def is_charged(self):
        return self.__charged

    def get_driver(self):
        return self.__driver

    def get_id(self):
        return self.__ID

    def __str__(self):
        return f"Driver number: {self.__ID}"


if __name__ == '__main__':
    for i in range(3):
        dr = Driver(3)
    print(*[(k, v) for (k, v) in Driver.__dict__.items()], sep='\n')
    dr.charge()
    print(*[(k, v) for (k, v) in dr.__dict__.items()], sep='\n')
    dr.discharge()
