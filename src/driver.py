from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


from info import BROWSER_FILE_PATH, WEBDRIVER_PATH, DRIVER_ARGUMENTS


class Driver:
    __BROWSER_FILE_PATH: str = BROWSER_FILE_PATH
    __WEBDRIVER_PATH: str = WEBDRIVER_PATH
    __DRIVER_ARGUMENTS: list = DRIVER_ARGUMENTS
    __DRIVERS_CREATED: int = 0

    def __new__(cls, *args, **kwargs):
        cls.__DRIVERS_CREATED += 1
        return super(Driver, cls).__new__(cls)

    def __init__(self,
                 wait_secs: int = 10):
        self.__wait_secs = wait_secs
        self.__charged = False
        self.__driver = None

    def charge(self, test=False):
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

    def discharge(self):
        if self.__charged:
            # input('Press to exit!')
            try:
                self.__charged = False
                self.__driver.close()
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


if __name__ == '__main__':
    for i in range(3):
        dr = Driver(3)
    print(*[(k, v) for (k, v) in Driver.__dict__.items()], sep='\n')
    dr.charge()
    print(*[(k, v) for (k, v) in dr.__dict__.items()], sep='\n')
    dr.discharge()
