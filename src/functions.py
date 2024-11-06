from pandas import DataFrame, read_html
from selenium.common import ElementNotInteractableException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep as time_sleep
from random import uniform as random_uniform
# from re import findall as re_findall
from re import search as re_search
from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardText, CF_UNICODETEXT, CloseClipboard
from pyautogui import hotkey as pyt_hotkey


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
    locator_xpath = ""

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
    if not PARSING_ERROR:
        print(f'Парсинг ДФ на текущей странице завершен В СТАНДАРТНОМ РЕЖИМЕ за <{counter}> циклов')
        df = get_total_df(df, appln_number_colname, ERROR_APPL_NUMBER, driver)
    appl_numbers = df[appln_number_colname].to_list()
    check_apl_numbs_duplicates = no_yes[len(appl_numbers) == len(set(appl_numbers))]
    # (06.09.2024)
    print(f'\nДУБЛИКАТЫ В ТАБЛИЦЕ ЗАЯВЛЕНИЙ ЭЛМК ОТСУТСТВУЮТ: <{check_apl_numbs_duplicates}>')

    df.to_excel(excel_temp_filename, index=False)

    return df, appl_numbers


def find_digits_after_text(driver, text_mark: str):
    html_source = driver.page_source

    digit = 0

    if text_mark in html_source:
        print(f'Искомый элемент <{text_mark}> ПРИСУТСТВУЕТ на странице!')
        match = re_search(f'{text_mark}(\d+)', html_source)
        if match:
            digit = int(match.group(1))
            print(f'Найдено число: <{digit}>')
            return (digit, True)
    else:
        print(f'Искомый элемент <{text_mark}> ОТСУТСТВУЕТ на странице!')
        return (digit, False)


def get_total_df(df, appln_number_colname, ERROR_APPL_NUMBER, driver):
    # удаляем пропущенные значения из общего ДФ !!!
    df, rows_df = parse_part_df(driver=driver,
                                need_delete_nans=True)
    # переводим номер заявления в целочисленное представление
    # df[appln_number_colname] = df[appln_number_colname].apply(lambda x: int(x))
    # ИСПРАВЛЕНИЕ 06.09.2024
    appl_numbers_lst = []
    for number in df[appln_number_colname].to_list():
        try:
            number_converted = int(number)
        # prevent ValueError: cannot convert float NaN to integer
        except ValueError:
            number_converted = ERROR_APPL_NUMBER
        appl_numbers_lst.append(number_converted)
    df[appln_number_colname] = appl_numbers_lst
    # DELETE ERRORS APPLS NUMBERS VALUES
    df = delete_df_rows_values(df, appln_number_colname, ERROR_APPL_NUMBER)
    print('Колонка с номерами заявлений успешно приведена к целочисленному значению!')
    return df.copy()


def parse_part_df(driver,
                  df_page_index: int = 1,
                  df_colnames_page_index: int = 0,
                  need_delete_nans: bool = True):
    # парсим таблицу со всем перечнем заявлений на получение ЭЛМК!!!
    # в переключателе выводить макисмальное количество строк по ЭЛМК!!!
    # подождать пока все строки прогрузятся!!!
    page_content_list = read_html(driver.page_source)
    df = DataFrame(page_content_list[df_page_index])
    # после аварийной перезагрузки сервером страницы
    # попытаемся выяснить тот же ДФ с заявлениями мы пытаемся спарсить или нет? 02.11.2024
    print(df.shape)
    df_colnames = list(DataFrame(page_content_list[df_colnames_page_index]))
    df.columns = df_colnames
    if need_delete_nans:
        df = delete_nan_rows(df=df)
    return df, df.shape[0]


def delete_nan_rows(df: DataFrame):
    # НАЧАЛО ФУНКЦИИ ---//---
    # НЕОБХОДИМО УЗНАТЬ КОЛИЧЕСТВО СТРОК СО ВСЕМИ ПРОПУЩЕННЫМИ ЗНАЧЕНИЯМИ (по всем колонкам)!!!
    idx = list(df.index[df.isnull().all(1)])
    print(idx)
    if idx:
        # кол-во удаляемых строк, а не одна строка!!!
        print(f'Необходимо удалить <{len(idx)}> строк ДФ!')
    print()
    print(f'Размерность ДФ ДО УДАЛЕНИЯ i строк: <{df.shape}>')
    print()
    # reset index???
    df.drop(idx, inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(f'Размерность ДФ ПОСЛЕ УДАЛЕНИЯ i строк: <{df.shape}>')
    return df
    # КОНЕЦ ФУНКЦИИ ---//---


def need_end_procedure(text_in):
    end_procedure = False
    text_in = text_in.lower().strip()
    if 'x' in text_in or 'х' in text_in:
        end_procedure = True
    return end_procedure


def delete_df_rows_values(df: DataFrame, colname: str, value):
    # НАЧАЛО ФУНКЦИИ ---//---
    # НЕОБХОДИМО УЗНАТЬ КОЛИЧЕСТВО СТРОК СО ВСЕМИ ПРОПУЩЕННЫМИ ЗНАЧЕНИЯМИ (по всем колонкам)!!!
    idx = list(df.index[df[colname] == value])
    print(idx)
    if idx:
        # кол-во удаляемых строк
        del_num_rows = len(idx)
        print(f'Необходимо удалить <{del_num_rows}> строк ДФ!')
        print()
        print(f'Размерность ДФ ДО УДАЛЕНИЯ i строк: <{df.shape}>')
        print()
        df.drop(idx, inplace=True)
        df.reset_index(drop=True, inplace=True)
        print(f'Размерность ДФ ПОСЛЕ УДАЛЕНИЯ <{del_num_rows}> строк: <{df.shape}>')
    return df


def move_2web_element(driver,
                      xpath,
                      timeout=3,
                      need_click: bool = False,
                      in_new_window: bool = False):
    # driver.refresh()
    # другой способ скроллинга сраницы попробовать!
    # сверять после каждой итерации количество записей на странице,
    # если оно не изменилось, пробуем скроллить еще!!!
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        return
    found_element = driver.find_element(By.XPATH, xpath)

    # прокручиваем страницу с помощью скрипта
    driver.execute_script("return arguments[0].scrollIntoView(true);", found_element)
    random_sleep(upper_bound=1.0, lower_bound=0)

    action = ActionChains(driver)
    if need_click:
        if in_new_window:
            action.move_to_element(found_element).perform()
            found_element.send_keys(Keys.COMMAND + 't')
        else:
            action.move_to_element(found_element).click().perform()
    else:
        action.move_to_element(found_element).perform()


def clipboard_copy(text: str, paste_value: bool = True):
    # в момент запуска данной функции окно загрузки файла - уже поверх остальных окон
    # этап копирования!
    counter = 0
    need_copy = True
    while need_copy and counter < 4:
        counter += 1
        try:
            OpenClipboard()
            EmptyClipboard()
            SetClipboardText(text, CF_UNICODETEXT)
            CloseClipboard()
            need_copy = False
        except:
            print("Ошибка при помещении объекта в буфер обмена!")
            print(f'Попытка номер: <{counter}>')
            time_sleep(2.5)
    if paste_value:
        # этап вставки
        pyt_hotkey('ctrl', 'v')
        # input('Сейчас будет нажата клавиша Enter')
        pyt_hotkey('enter')
    else:
        print(f'Текст <{text}> - помещен в буфер обмена!!!')
