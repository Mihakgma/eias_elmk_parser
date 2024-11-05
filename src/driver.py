from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


from info import BROWSER_FILE_PATH, WEBDRIVER_PATH, DRIVER_ARGUMENTS


class Driver:
    __BROWSER_FILE_PATH = BROWSER_FILE_PATH
    __WEBDRIVER_PATH = WEBDRIVER_PATH
    __DRIVER_ARGUMENTS = DRIVER_ARGUMENTS
    __DRIVERS_CREATED = 0

    def __new__(cls, *args, **kwargs):
        cls.__DRIVERS_CREATED += 1
        return super(Driver, cls).__new__(cls)

    def __init__(self,
                 wait_secs: int = 10):
        self.wait_secs = wait_secs
        self.__charged = False

    def charge(self):
        print(f"Driver number: <{self.__DRIVERS_CREATED}> has been initiated.")
        options = webdriver.ChromeOptions()
        ###
        for args in DRIVER_ARGUMENTS:
            options.add_argument(args)
        ###
        options.binary_location = self.__BROWSER_FILE_PATH
        try:
            driver = webdriver.Chrome(executable_path=self.__WEBDRIVER_PATH,
                                      options=options)
            driver.implicitly_wait(self.wait_secs)
            self.__charged = True
        except TypeError as e:
            print(e)
            print("Selenium driver error: probably versions conflict...")

    def is_charged(self):
        return self.__charged


if __name__ == '__main__':
    for i in range(3):
        dr = Driver(3)
    print(*[(k, v) for (k, v) in Driver.__dict__.items()], sep='\n')
    dr.charge()
    print(*[(k, v) for (k, v) in dr.__dict__.items()], sep='\n')
