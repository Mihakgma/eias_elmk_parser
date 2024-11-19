import tqdm
from pandas import DataFrame
from selenium.common.exceptions import StaleElementReferenceException

from classes.check_dates import DateChecker
from classes.data_manager import DataManager
from classes.threads_monitoring import ThreadsMonitor
from functions.df_functions import excel_to_data_frame_parser, printDimensionsOfDF
from classes.driver import Driver
from functions.parsing_functions import (send_keys_by_xpath, parse_total_df, need_end_procedure, random_sleep,
                                         find_element_xpath, parse_part_df, move_2web_element, get_personal_data,
                                         click_element_by_xpath, get_page_text, is_text_on_page, submit_certificate)
from data import (HOME_URL, LOGIN_XPATH, LOGIN, PASSWORD_XPATH, PASSWORD, ELMK_URL, TEMP_XLSX_FILENAME,
                  APPLN_NUMBER_COLNAME, NUM_ROWS_MARK, NO_or_YES, NAVIGATOR_STATUS, START_KEY_WORD, OK_CERT_SCREEN_FILE,
                  CERT_SCREEN_FILE)
from patterns.setter_logger import setter_log


class Navigator:
    """
    need to think about this class:
    1) overriding __str__ method (to save all fields of Navigator instance):
        a) before calling clear_memory();
        b) after calling clear_memory();
        Why?
        Cause maybe it would be useful to remember the shapes of the DFs
        or also save min-max dates of the applications from DFs
        or maybe another data from DFs???
        which contain in Navigator instance...
    """
    WARNINGS = {
        HOME_URL: [print, 'Confirm certificate and enter any key to continue.'],
        ELMK_URL: [input, 'Use previously downloaded DF: да (y) / нет (n)?'],
    }
    __STATUS = NAVIGATOR_STATUS
    __START_KEY_WORD = START_KEY_WORD
    __CERT_SCREEN_FILE = CERT_SCREEN_FILE
    __OK_CERT_SCREEN_FILE = OK_CERT_SCREEN_FILE

    def __init__(self):
        print(self.__class__.__name__ + " initialized")
        self.__driver_obj = None
        self.__current_url: str = "_"
        self.__current_application_number: int = -1
        self.__left_df: DataFrame = DataFrame()
        self.__appl_numbers: list = []
        self.__right_df: DataFrame = DataFrame()
        self.__status: int = 1

    def get_driver_obj(self) -> Driver:
        return self.__driver_obj

    def set_driver_obj(self, driver: Driver):
        self.__driver_obj = driver

    def get_current_url(self):
        return self.__current_url

    @setter_log("LOGS")
    def set_current_url(self, url: str):
        self.__current_url = url

    def get_current_application_number(self):
        return self.__current_application_number

    @setter_log("LOGS")
    def set_current_application_number(self, number: int):
        self.__current_application_number = number

    def get_status(self) -> int:
        return self.__status

    def set_status(self, status: int):
        if status in self.__STATUS:
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

    def navigate(self, page_path):
        driver = self.__driver_obj.get_driver()
        self.__current_url = driver.current_url
        driver.get(page_path)
        self.print_page()
        warnings = self.WARNINGS
        if page_path in warnings:
            func, warn_text = warnings[page_path][0], warnings[page_path][1]
            if page_path == HOME_URL:
                submit_certificate(cert_screen_file_path=CERT_SCREEN_FILE,
                                   ok_screen_file_path=OK_CERT_SCREEN_FILE,
                                   counter=5)
            return func(warn_text)

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
        input("Logged in. Press Enter to continue...")
        is_text_on_page(driver=self.__driver_obj.get_driver(),
                        text=self.__START_KEY_WORD)
        self.__current_url = driver.current_url
        self.status = 2
        # input('Подождать пока страница прогрузится?')
        answer = self.navigate(ELMK_URL).strip().lower()
        self.status = 3
        if "y" in answer or "да" in answer:
            appl_df = excel_to_data_frame_parser(file=TEMP_XLSX_FILENAME,
                                                 sheet_name="Sheet1",
                                                 rows_to_skip=0,
                                                 blank_values_drop=0,
                                                 first_row_header=0)
            printDimensionsOfDF(dfInput=appl_df,
                                warnStr="подгрузки временного ранее сохраненного ДФ")
            appl_numbers = appl_df[APPLN_NUMBER_COLNAME].to_list()
        else:
            appl_df, appl_numbers = parse_total_df(driver=driver,
                                                   num_rows_mark=NUM_ROWS_MARK,
                                                   appln_number_colname=APPLN_NUMBER_COLNAME,
                                                   no_yes=NO_or_YES,
                                                   excel_temp_filename=TEMP_XLSX_FILENAME,
                                                   sleep_secs_up_to=1.2,
                                                   counter_max_value=350,
                                                   ask_for_cancel_interval=100)
        self.__left_df = appl_df
        self.__appl_numbers = appl_numbers
        self.__current_url = driver.current_url
        self.status = 4

    def parse_personal_data(self,
                            ask_for_cancel_interval=5000,
                            sleep_secs_up_to=1.1,
                            sleep_secs_up_to_pesr_data=0.5):

        # %%time
        # ask_for_cancel_interval - периодичность по количеству заявлений - запрос на завершение процедуры
        browser = self.__driver_obj.get_driver()
        appl_numbers = self.__appl_numbers
        # element_found = False
        browser.refresh()
        self.__current_url = browser.current_url
        self.status = 5
        appl_dict = {}
        counter = 0
        stop_parsing = False
        for number in tqdm.tqdm(appl_numbers):
            self.set_current_application_number(number=number)
            self.set_current_url(url=browser.current_url)
            # переименовать флаг!!!
            if stop_parsing:  # завершаем досрочно, если юзер ввел х (русс / англ. раскладка)
                break
            need_parse_appl = True
            tries = 0
            while need_parse_appl:
                tries += 1
                if abs(tries) % 5 == 0:
                    print(f"Trying to refresh homepage <{ELMK_URL}> on try number <{tries}>")
                    browser.get(url=ELMK_URL)
                if counter % ask_for_cancel_interval == 0:
                    if need_end_procedure(text_in=input('для отмены процесса парсинга введите х')):
                        print('Процесс - прерван ...')
                        stop_parsing = True
                        # need_parse_appl = False
                        break
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
                            # print(f'Пропуск парсинга по номеру: <{number}>')
                            # весь код после слова "continue" - не будет выполнен на данной итерации!
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
            # ПОЛУЧАЕМ ПЕРСОНАЛЬНЫЕ ДАННЫЕ!
            if not stop_parsing:
                appl_dict[number] = get_personal_data(driver=browser,
                                                      sleep_up_to=sleep_secs_up_to_pesr_data,
                                                      in_new_window=True)

        print(f'\nКоличество спарсенных строк таблицы заявлений составило: <{len(appl_dict)}>')
        self.__right_df = DataManager.preprocess_personal_df(appl_dict)

    def clear_memory(self, all_data: bool = False):
        self.__left_df = DataFrame()
        self.__appl_numbers = []
        if all_data:
            self.__right_df = DataFrame()

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
        # self.print_page()
        # input("Navigator has been called. Press Enter to continue...")
        self.navigate(HOME_URL)
        self.login()
        input("DF with general data has been parsed. Press Enter to continue...")
        threads_monitoring = ThreadsMonitor()
        threads_monitoring.close_self()
        # random_sleep(upper_bound=40, lower_bound=25)
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
    print(navigator.status)
