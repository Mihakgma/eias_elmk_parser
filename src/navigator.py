from pandas import DataFrame

from df_functions import excel_to_data_frame_parser, printDimensionsOfDF
from driver import Driver
from functions import send_keys_by_xpath, parse_total_df
from info import HOME_URL, LOGIN_XPATH, LOGIN, PASSWORD_XPATH, PASSWORD, ELMK_URL, TEMP_XLSX_FILENAME, \
    APPLN_NUMBER_COLNAME, NUM_ROWS_MARK, NO_or_YES
from singleton import Singleton


class Navigator(Singleton):
    WARNINGS = {
        HOME_URL: [input, 'Confirm certificate and enter any key to continue.'],
        ELMK_URL: [input, 'Use previously downloaded DF: да (y) / нет (n)?'],
    }

    def __init__(self, driver: Driver):
        self.__driver = driver
        self.__current_url = "_"
        self.__current_application_number = -1
        self.__appl_df = DataFrame()
        self.__appl_numbers = []
        self.__appl_total_df = DataFrame()

    def get_driver(self) -> Driver:
        return self.__driver

    def get_current_url(self):
        return self.__current_url

    def get_current_application_number(self):
        return self.__current_application_number

    def navigate(self, page_path):
        driver = self.__driver.get_driver()
        self.__current_url = driver.current_url
        driver.get(page_path)
        warnings = self.WARNINGS
        if page_path in warnings:
            func, warn_text = warnings[page_path][0], warnings[page_path][1]
            return func(warn_text)

    def login(self):
        driver = self.__driver.get_driver()
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
        answer = self.navigate(ELMK_URL).strip().lower()
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
        self.__appl_df = appl_df
        self.__appl_numbers = appl_numbers
        # подождать (?) пока контент прогрузится...


if __name__ == '__main__':
    navigator = Navigator(Driver())
    print(navigator.get_current_url())
    print(navigator.get_current_application_number())
