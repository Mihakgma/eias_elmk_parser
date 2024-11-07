from os import path as os_path
from threading import Thread
from time import sleep as time_sleep
from os import makedirs as os_makedirs

from check_dates import DateChecker
from driver import Driver
from function_invoker import Invoker
from injector import Injector
from navigator import Navigator


class TextCaching(Thread):
    __METHODS_CLASSES = {
        'Navigator': ['get_current_url',
                      'get_current_application_number']
    }
    __GET_DRIVER_METHOD_NAME = 'get_driver'
    __START_RUN_MESSAGE = "Starting text caching thread at"
    __STOP_RUN_MESSAGE = "Stopping text caching thread at"

    def __init__(self,
                 cache_dir="..\\text_data",
                 text_filename_format=".txt",
                 sleep_time: int = 1,
                 obj: object = None,
                 max_iterations: int = 5):
        Thread.__init__(self)
        self.cache_dir = cache_dir
        self.text_filename_format = text_filename_format
        self.sleep_time = sleep_time
        self.__obj = obj
        self.__max_iterations = max_iterations
        self.__text_info = {}

    def run(self):
        print(DateChecker.get_nowTS_messaged(text=self.__START_RUN_MESSAGE))
        obj = self.__obj
        obj_class_name = obj.__class__.__name__
        get_driver_method_name = self.__GET_DRIVER_METHOD_NAME
        # can we get driver from obj?
        does_contain_driver = any([get_driver_method_name == k for k in obj.__class__.__dict__])
        if obj is None or obj_class_name not in self.__METHODS_CLASSES:
            print(f"Class of input <{obj_class_name}> IS OUT OF check list.")
        elif does_contain_driver and obj_class_name in self.__METHODS_CLASSES:
            print(f"Class of input <{obj_class_name}> IS IN the check list.")
            print(f'We can get driver from obj: <{obj}>')
            print("starting a new thread...")
            max_iter = self.__max_iterations
            counter = 0
            invoker = Invoker(obj, get_driver_method_name)
            is_driver_charged = invoker().is_charged()
            while counter < max_iter and is_driver_charged:
                is_driver_charged = invoker().is_charged()
                counter += 1
                time_sleep(self.sleep_time)
                self.save_text()
        else:
            print("Cannot start text caching...")
            print(f"Probably class of input <{obj_class_name}> IS NOT IN CHECK LIST.")
        print(DateChecker.get_nowTS_messaged(text=self.__STOP_RUN_MESSAGE))

    def save_text(self):
        classes_dict = self.__METHODS_CLASSES
        obj = self.__obj
        obj_class_name = obj.__class__.__name__
        text_info = {}
        for method_name in classes_dict[obj_class_name]:
            invoker = Invoker(obj, method_name)
            text_value = str(invoker())
            print(method_name)
            print(text_value)
            full_path = os_path.join(self.cache_dir,
                                     method_name.replace("get_", "") + self.text_filename_format)
            text_info[text_value] = full_path
        self.__text_info = text_info
        # we can comment the following code
        # if we don't want to save text_info dict results on hard drive
        try:
            os_makedirs(self.cache_dir)
        except FileExistsError:
            pass
        for text_value, full_path in text_info.items():
            print(f'<{text_value}> store in {full_path}>')
            with open(full_path, "w") as file:
                file.write(text_value)


if __name__ == '__main__':
    driver_1 = Driver()
    driver_1.charge(test=True)
    navigator_1 = Navigator()
    injector = Injector(driver_1, navigator_1, auto_charging=False)
    injector.inject()
    text_caching = TextCaching(sleep_time=3, obj=navigator_1)
    text_caching.start()
    time_sleep(5)
    driver_1.discharge()
    time_sleep(15)
    print(DateChecker.get_nowTS_messaged(text="Last message at"))
