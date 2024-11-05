from selenium.common import ElementNotInteractableException, TimeoutException
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
