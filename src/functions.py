from pandas import DataFrame
from selenium.common import ElementNotInteractableException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep as time_sleep
from random import uniform as random_uniform


def random_sleep(upper_bound: int, lower_bound=0):
    random_digit_parse = random_uniform(lower_bound, upper_bound)
    time_sleep(random_digit_parse)


def send_keys_by_xpath(driver,
                       xpath,
                       text,
                       pause_secs=2.1,
                       timeout=15,
                       need_press_enter: bool = False):
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        return
    found_element = driver.find_element(By.XPATH, xpath)
    try:
        found_element.send_keys(text)
        if need_press_enter:
            random_sleep(upper_bound=pause_secs)
            found_element.send_keys(Keys.ENTER)
    except ElementNotInteractableException:
        print(f'Невозможно отправить текст: <{text}>')
        print(f'В форму или элемент: <{found_element}>')
        clipboard_copy(text=str(text), paste_value=False)
        input('Исправьте, пожалуйста, в ручную, а затем нажмите Enter для продолжения ввода информации по ЭИ!')


def parse_total_df(driver,
                   num_rows_mark: str,
                   appln_number_colname: str,
                   no_yes: str,
                   excel_temp_filename: str,
                   sleep_secs_up_to: float = 1.5,
                   counter_max_value: int = 150,
                   ask_for_cancel_interval: int = 50):
    """
    Парсит всю таблицу с переводом ее в pandas-ДФ
    Возвращает ДФ и номера заявлений (в виде листа)
    """
    ERROR_APPL_NUMBER = -666
    driver.refresh()
    time_sleep(7)
    num_rows, num_rows_is_available = find_digits_after_text(driver=driver,
                                                             text_mark=num_rows_mark)
    print(num_rows, num_rows_is_available)

    counter = 0
    rows_df = 0
    need_parse_page = True
    PARSING_ERROR = False
    df = DataFrame(dict())

    try:
        while need_parse_page and counter < counter_max_value:
            counter += 1
            df = get_total_df(df, appln_number_colname, ERROR_APPL_NUMBER, driver)
            if counter % ask_for_cancel_interval == 0:
                if need_end_procedure(text_in=input('для отмены процесса парсинга введите х')):
                    need_parse_page = False
            if rows_df >= num_rows:
                print(f'\nСпарсили ВСЕ строки ДФ <{rows_df}> в ДОЛЖНОМ количестве <{num_rows}>!')
                need_parse_page = False
            else:
                print(f'\nСпарсили НЕ ВСЕ строки ДФ <{rows_df}> в ДОЛЖНОМ количестве <{num_rows}>!')

                random_sleep(upper_bound=sleep_secs_up_to)
                df, rows_df = parse_part_df(driver=driver,
                                            need_delete_nans=False)
                # ИСПРАВЛЕНИЕ ОТ 06.09.2024!!!
                # ПРОВЕРКА НА ПУСТОЕ ЗНАЧЕНИЕ № ЗАЯВЛЕНИЯ
                is_number_empty = True
                tries = 0
                while is_number_empty and tries < 15:
                    tries += 1
                    try:
                        locator_xpath = f"//*[contains(text(), '{int(df.iloc[df.shape[0] - tries, 1])}')]"
                        is_number_empty = False
                    # ValueError: cannot convert float NaN to integer
                    except ValueError:
                        pass
                # скроллим страницу вниз по последнему отображенному номеру заявления в таблице!!!
                try:
                    move_2web_element(driver=driver, xpath=locator_xpath)
                except StaleElementReferenceException:
                    pass
    except BaseException as error:
        print('Caught this error: ' + repr(error))
        print(f'Парсинг ДФ на текущей странице завершен В АВАРИЙНОМ РЕЖИМЕ за <{counter}> циклов')
        PARSING_ERROR = True
    if PARSING_ERROR == False:
        print(f'Парсинг ДФ на текущей странице завершен В СТАНДАРТНОМ РЕЖИМЕ за <{counter}> циклов')
        df = get_total_df(df, appln_number_colname, ERROR_APPL_NUMBER, driver)
    appl_numbers = df[appln_number_colname].to_list()
    check_apl_numbs_duplicates = no_yes[len(appl_numbers) == len(set(appl_numbers))]
    # (06.09.2024)
    print(f'\nДУБЛИКАТЫ В ТАБЛИЦЕ ЗАЯВЛЕНИЙ ЭЛМК ОТСУТСТВУЮТ: <{check_apl_numbs_duplicates}>')

    df.to_excel(excel_temp_filename, index=False)

    return df, appl_numbers
