import json

import tqdm
from pandas import DataFrame
from selenium.common.exceptions import StaleElementReferenceException

from os import path as os_path
from os import makedirs as os_makedirs

from classes.check_dates import DateChecker
from classes.data_manager import DataManager
from classes.threads_monitoring import ThreadsMonitor
from functions.df_functions import excel_to_data_frame_parser, printDimensionsOfDF
from classes.driver import Driver
from functions.parsing_functions import (send_keys_by_xpath, parse_total_df, random_sleep,
                                         find_element_xpath, parse_part_df, move_2web_element, get_personal_data,
                                         click_element_by_xpath, get_page_text, submit_certificate)
from data import (HOME_URL, LOGIN_XPATH, LOGIN, PASSWORD_XPATH, PASSWORD, ELMK_URL, TEMP_XLSX_FILENAME,
                  APPLN_NUMBER_COLNAME, NUM_ROWS_MARK, NO_or_YES, NAVIGATOR_STATUS, START_KEY_WORD, OK_CERT_SCREEN_FILE,
                  CERT_SCREEN_FILES, LOGS_DIR, NAVIGATOR_SERIALIZE_FILE, COLNAMES_DICT, PERS_DATA_XPATH,
                  FILTER_BUTTON_XPATH, FILTER_APPL_NUMBER_INPUT_XPATH, FILTER_APPL_SUBMIT_BUTTON_XPATH)
from patterns.browser_error_wrapper import handle_exceptions_quit_driver
from patterns.setter_logger import setter_log


class Navigator:
    """
    this class is used to navigate through web pages
    and saving parsed data to excel and json file
    after successful navigation or even if exception occurs...
    """
    WARNINGS = {
        HOME_URL: [print, 'Confirm certificate and enter any key to continue.'],
    }
    __STATUS: dict = NAVIGATOR_STATUS
    __START_KEY_WORD: str = START_KEY_WORD
    __CERT_SCREEN_FILES: list = CERT_SCREEN_FILES
    __OK_CERT_SCREEN_FILE: str = OK_CERT_SCREEN_FILE
    __CERT_TRIES: int = 7
    __COLNAMES_DICT = COLNAMES_DICT
    __PERS_DATA_XPATH = PERS_DATA_XPATH

    def __init__(self):
        print(self.__class__.__name__ + " initialized")
        self.__driver_obj = None
        self.__current_url: str = "_"
        self.__current_application_number: int = -1
        self.__left_df: DataFrame = DataFrame()
        self.__appl_numbers: list = []
        self.__right_df: DataFrame = DataFrame()
        self.__status: int = 1
        self.__need_parse_left_df = False
        self.__right_df_dict = {}
        self.__personal_data_by_filter = False

    def set_personal_data_by_filter(self, personal_data_by_filter: bool):
        if type(personal_data_by_filter) is not bool:
            raise TypeError(f"Cannot set 'personal_data_by_filter' field to {type(personal_data_by_filter)}")
        getting_personal_data_approach = [
            "by scrolling left DF",
            "by using filter"
        ]
        print(f"Getting personal data has been changed to <{getting_personal_data_approach[personal_data_by_filter]}>")
        self.__personal_data_by_filter = personal_data_by_filter

    def get_personal_data_by_filter(self):
        return self.__personal_data_by_filter

    def set_need_parse_left_df(self, need_parse_left_df: bool):
        if type(need_parse_left_df) is not bool:
            raise TypeError(f"Cannot set 'need_parse_left_df' field to {type(need_parse_left_df)}")
        self.__need_parse_left_df = need_parse_left_df

    def get_driver_obj(self) -> Driver:
        return self.__driver_obj

    def set_driver_obj(self, driver: Driver):
        if type(driver) is not Driver:
            raise TypeError(f"cannot set driver of {type(driver)} type to a <{self.__class__.__name__}> instance")
        driver.set_linked_navigator(self)
        self.__driver_obj = driver

    def get_current_url(self):
        return self.__current_url

    @setter_log(LOGS_DIR)
    def set_current_url(self, url: str):
        if type(url) is not str:
            raise TypeError(f"cannot set url of {type(url)} type to a <{self.__class__.__name__}> instance")
        self.__current_url = url

    def get_current_application_number(self):
        return self.__current_application_number

    @setter_log(LOGS_DIR)
    def set_current_application_number(self, number: int):
        if type(number) is not int:
            raise TypeError(f"Cannot set application number of {type(number)} type")
        elif number < -1:
            raise ValueError(f"Cannot set negative application number: <{number}>")
        # print(number)
        self.__current_application_number = number

    def get_status(self) -> int:
        return self.__status

    @setter_log(LOGS_DIR)
    def set_status(self, status: int):
        if status in self.__STATUS:
            print(f"Status: <{status}>")
            self.__status = status
        else:
            message = "Status must be one of the following:\n" + \
                      "\n".join([f"{k}: {v}" for (k, v) in self.__STATUS.items()])
            raise ValueError(message)

    status = property(get_status, set_status)

    def print_page(self):
        driver = self.__driver_obj.get_driver()
        text = get_page_text(driver)
        try:
            print(f"\n---///---\nPrinting page:<{driver.current_url}> "
                  f"contents:\n{text}\n---///---")
        except AttributeError as e:
            print(e)

    @handle_exceptions_quit_driver
    def navigate(self, page_path):
        try:
            driver = self.__driver_obj.get_driver()

            self.set_current_url(driver.current_url)
            if page_path == HOME_URL:
                submit_certificate(cert_screen_files_path=CERT_SCREEN_FILES,
                                   ok_screen_file_path=OK_CERT_SCREEN_FILE,
                                   counter=5)
            driver.get(page_path)
            self.set_current_url(driver.current_url)
            warnings = self.WARNINGS
            if page_path in warnings:
                func, warn_text = warnings[page_path][0], warnings[page_path][1]
                return func(warn_text)
        except AttributeError as e:
            print(f"navigate method failed with <{e}>")
            return

    @handle_exceptions_quit_driver
    def login(self):
        driver = self.__driver_obj.get_driver()
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
        print("Logged in. Press Enter to continue...")
        self.set_current_url(driver.current_url)
        self.set_status(2)
        self.navigate(ELMK_URL)
        self.set_status(3)
        if self.__need_parse_left_df:
            appl_df, appl_numbers = parse_total_df(driver=driver,
                                                   num_rows_mark=NUM_ROWS_MARK,
                                                   appln_number_colname=APPLN_NUMBER_COLNAME,
                                                   no_yes=NO_or_YES,
                                                   excel_temp_filename=TEMP_XLSX_FILENAME,
                                                   sleep_secs_up_to=1.2,
                                                   counter_max_value=350,
                                                   ask_for_cancel_interval=100)
            self.__appl_numbers = appl_numbers
        else:
            appl_df = excel_to_data_frame_parser(file=TEMP_XLSX_FILENAME,
                                                 sheet_name="Sheet1",
                                                 rows_to_skip=0,
                                                 blank_values_drop=0,
                                                 first_row_header=0)
            printDimensionsOfDF(dfInput=appl_df,
                                warnStr="downloading left DF from excel", )
            if len(self.__appl_numbers) == 0:
                self.__appl_numbers = appl_df[APPLN_NUMBER_COLNAME].to_list()

        self.__left_df = appl_df
        self.set_current_url(driver.current_url)
        self.set_status(4)

    def set_appl_numbers(self, appl_numbers: list):
        if type(appl_numbers) is not list:
            raise TypeError(f"Cannot set 'appl_numbers' field to {type(appl_numbers)}")
        self.__appl_numbers = appl_numbers

    def get_appl_numbers(self):
        return self.__appl_numbers

    @handle_exceptions_quit_driver
    def parse_personal_data_by_filter(self,
                                      sleep_secs_up_to=1.1,
                                      sleep_secs_up_to_pesr_data=0.5):
        """
        This method is gonna be used to parse the personal data
        with help of filtering on the page with left DF...
        :param sleep_secs_up_to:
        :param sleep_secs_up_to_pesr_data:
        :return:
        """
        browser = self.__driver_obj.get_driver()
        appl_numbers = self.__appl_numbers
        browser.refresh()
        self.__current_url = browser.current_url
        self.set_status(5)
        appl_dict = self.__right_df_dict
        stop_parsing = False
        ind = -1
        for number in tqdm.tqdm(appl_numbers):
            ind += 1
            random_sleep(int(sleep_secs_up_to))
            if number in appl_dict:
                self.set_status(15)
                # appl_number_dict = appl_dict[number]
                # if all([str(v).replace("null", "") == ""
                #         for (k, v) in appl_number_dict.items()]):
                #     self.set_status(16)
                pass
            self.set_current_application_number(number)
            self.set_current_url(browser.current_url)
            if stop_parsing:
                break
            filter_found = find_element_xpath(driver=browser,
                                              xpath=FILTER_APPL_SUBMIT_BUTTON_XPATH)
            print("Submit filter button search has been ended...")
            if not filter_found:
                self.set_status(17)
                print("Submit filter button has not been found")
                click_element_by_xpath(driver=browser,
                                       xpath=FILTER_BUTTON_XPATH,
                                       timeout=15,
                                       in_new_window=False)
                print("Filter button has been clicked")
            send_keys_by_xpath(driver=browser,
                               xpath=FILTER_APPL_NUMBER_INPUT_XPATH,
                               text=number,
                               pause_secs=2.1,
                               timeout=15,
                               need_press_enter=False,
                               need_clear_input=True)
            click_element_by_xpath(driver=browser,
                                   xpath=FILTER_APPL_SUBMIT_BUTTON_XPATH,
                                   timeout=15,
                                   in_new_window=False)
            click_element_by_xpath(driver=browser,
                                   xpath=FILTER_BUTTON_XPATH,
                                   timeout=15,
                                   in_new_window=False)
            # answer = input(f"Enter x to stop parsing <{number}>").lower().strip()
            # if answer == "x" or answer == "х":
            appl_xpath = f"//*[contains(text(), '{number}')]"
            number_found = find_element_xpath(driver=browser,
                                              xpath=appl_xpath)
            print(f"Number <{number}> has been found on the page: <{number_found}>")
            if not number_found:
                try:
                    self.__appl_numbers = appl_numbers[ind + 1:]
                except IndexError:
                    stop_parsing = True
                    print("list __appl_numbers out of range")
            if not stop_parsing and number_found:
                click_element_by_xpath(driver=browser,
                                       xpath=appl_xpath,
                                       timeout=15,
                                       in_new_window=True)
                appl_dict[number] = get_personal_data(driver=browser,
                                                      COLNAMES_DICT=self.__COLNAMES_DICT,
                                                      PERS_DATA_XPATH=self.__PERS_DATA_XPATH,
                                                      sleep_up_to=sleep_secs_up_to_pesr_data,
                                                      in_new_window=True)
                self.__right_df_dict = appl_dict
                try:
                    self.__appl_numbers = appl_numbers[ind + 1:]
                except IndexError:
                    stop_parsing = True
                    print("list __appl_numbers out of range")
        print(f'\nКоличество спарсенных строк таблицы заявлений составило: <{len(appl_dict)}>')
        self.__right_df = DataManager.preprocess_personal_df(appl_dict)

    @handle_exceptions_quit_driver
    def parse_personal_data(self,
                            sleep_secs_up_to=1.1,
                            sleep_secs_up_to_pesr_data=0.5):
        browser = self.__driver_obj.get_driver()
        appl_numbers = self.__appl_numbers
        browser.refresh()
        self.__current_url = browser.current_url
        self.set_status(5)
        appl_dict = self.__right_df_dict
        counter = 0
        stop_parsing = False
        ind = -1
        for number in tqdm.tqdm(appl_numbers):
            ind += 1
            appl_number_dict = appl_dict[number]
            if all([str(v).replace("null", "") == ""
                    for (k, v) in appl_number_dict.items()]):
                pass
            self.set_current_application_number(number)
            self.set_current_url(browser.current_url)
            if stop_parsing:
                break
            need_parse_appl = True
            tries = 0
            while need_parse_appl:
                tries += 1
                if abs(tries) % 5 == 0:
                    print(f"Trying to refresh homepage <{ELMK_URL}> on try number <{tries}>")
                    browser.get(url=ELMK_URL)
                print(number)
                counter += 1
                try:
                    appl_xpath = f"//*[contains(text(), '{number}')]"
                    random_sleep(upper_bound=sleep_secs_up_to)
                    element_found = find_element_xpath(driver=browser,
                                                       xpath=appl_xpath)
                    try:
                        if element_found:
                            pass
                        else:  # ссылка (по XPath) на заявление не найдена!
                            need_scroll_down = True
                            while need_scroll_down:
                                df_temp, rows_df = parse_part_df(driver=browser,
                                                                 need_delete_nans=False)
                                locator_xpath = f"//*[contains(text(), '{int(df_temp.iloc[df_temp.shape[0] - 1, 1])}')]"
                                # скроллим страницу вниз по последнему отображенному номеру заявления в таблице!!!
                                move_2web_element(driver=browser, xpath=locator_xpath)
                                element_found = find_element_xpath(driver=browser,
                                                                   xpath=appl_xpath)
                                if element_found:
                                    need_scroll_down = False
                            # continue
                    except IndexError:
                        random_sleep(upper_bound=15, lower_bound=5)
                    except ValueError:
                        browser.refresh()
                        random_sleep(upper_bound=10, lower_bound=3)
                        browser.get(url=ELMK_URL)
                        random_sleep(upper_bound=5, lower_bound=3)

                    click_element_by_xpath(driver=browser,
                                           xpath=appl_xpath,
                                           timeout=15,
                                           in_new_window=True)
                    need_parse_appl = False

                except StaleElementReferenceException:
                    pass
            if not stop_parsing:
                appl_dict[number] = get_personal_data(driver=browser,
                                                      COLNAMES_DICT=self.__COLNAMES_DICT,
                                                      PERS_DATA_XPATH=self.__PERS_DATA_XPATH,
                                                      sleep_up_to=sleep_secs_up_to_pesr_data,
                                                      in_new_window=True)
            self.__right_df_dict = appl_dict
            try:
                self.__appl_numbers = appl_numbers[ind + 1:]
            except IndexError:
                stop_parsing = True
                print("list __appl_numbers out of range")
        print(f'\nКоличество спарсенных строк таблицы заявлений составило: <{len(appl_dict)}>')
        self.__right_df = DataManager.preprocess_personal_df(appl_dict)

    def clear_memory(self, all_data: bool = False):
        self.__left_df = DataFrame()
        self.__appl_numbers = []
        if all_data:
            self.__right_df = DataFrame()

    def serialize(self):
        print(f"\nSerializing process for <{self}>\nhas been initiated...\n")
        """Serializes the Navigator object to a JSON file."""
        data_to_serialize = {
            "__status": self.__status,
            "__appl_numbers": self.__appl_numbers,
            "__right_df_dict": self.__right_df_dict,
        }
        try:  # Handle potential errors during serialization
            fullpath_json = os_path.join(LOGS_DIR, NAVIGATOR_SERIALIZE_FILE)
            os_makedirs(LOGS_DIR, exist_ok=True)
            with open(fullpath_json, "w", encoding='utf-8') as f:
                json.dump(data_to_serialize, f, indent=4)
            print(f"Navigator data SERIALIZED successfully to <{NAVIGATOR_SERIALIZE_FILE}>")
        except Exception as e:
            print(f"Error during serialization: {e}")

    def deserialize(self):
        try:
            fullpath_json = os_path.join(LOGS_DIR, NAVIGATOR_SERIALIZE_FILE)
            with open(fullpath_json, "r", encoding='utf-8') as f:
                j = json.load(f)
            print("\nRead json-file:")
            # [print(key, val) for key, val in j.items()]
            [setattr(self, key, val) for key, val in j.items()
             if hasattr(self, key)]
            cls_name = "_" + self.__class__.__name__
            [setattr(self, cls_name + key, val) for key, val in j.items()
             if hasattr(self, cls_name + key)]
            print(f"Navigator data DESERIALIZED successfully FROM <{NAVIGATOR_SERIALIZE_FILE}>")
            self.set_status(12)
        except Exception as e:
            print(f"Error during deserialization: {e}")

    def __str__(self):
        driver = self.__driver_obj
        class_name = self.__class__.__name__
        ts_text = f"\nAt time ({class_name}): "
        out = [
            f"{DateChecker.get_nowTS_messaged(text=ts_text)}",
            f"driver ID = <{driver.get_id()}>",
            f"driver is charged: <{driver.is_charged()}>",
            f"current URL: <{self.__current_url}>,",
            f"current application number: <{self.__current_application_number}>,",
            f"left (general data) table shape: <{self.__left_df.shape}>",
            f"applications (numbers) in instance: <{len(self.__appl_numbers)}>",
            f"right (personal data) table shape: <{self.__right_df.shape}>"
        ]
        return ";\n".join(out)

    def __call__(self, *args, **kwargs):
        with self.__driver_obj.get_driver():
            threads_monitoring = ThreadsMonitor()
            threads_monitoring.start()
            self.navigate(HOME_URL)
            threads_monitoring.stop()
            self.login()
            print("DF with general data has been parsed. Press Enter to continue...")
            if self.get_personal_data_by_filter():
                # self.parse_personal_data_by_filter(**kwargs)
                self.parse_personal_data_by_filter()
            else:
                self.parse_personal_data(**kwargs)


if __name__ == '__main__':
    driver_1 = Driver()
    driver_1.charge()
    navigator = Navigator()
    navigator.set_driver_obj(driver_1)
    print(navigator.get_current_url())
    print(navigator.get_current_application_number())
    print(navigator)
    navigator.clear_memory()
    print(navigator)
    # navigator.status = 999
    print(navigator.get_status())
    applications_test = [1, 2, 3, 4, '', "sdfsd", True, False]
    navigator.set_appl_numbers(applications_test)
    navigator.serialize()
    print(navigator)
    print(navigator.get_appl_numbers())
    navigator_1 = Navigator()
    navigator_1.set_driver_obj(driver_1)
    navigator_1.deserialize()
    print(navigator_1)
    print(navigator_1.get_appl_numbers())
