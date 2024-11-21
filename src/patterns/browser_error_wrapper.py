import functools
from selenium.common.exceptions import NoSuchWindowException, WebDriverException

from classes.driver import Driver


def handle_exceptions_quit_driver(func):
    """Decorator for browser exceptions handling"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        last_word = "Press any key to quit webdriver..."
        try:
            return func(*args, **kwargs)
        except NoSuchWindowException as e:
            __print_error_discharge_driver(e, last_word)
            return None
        except WebDriverException as wde:
            __print_error_discharge_driver(wde, last_word)
            return None
        except TypeError as te:
            __print_error_discharge_driver(te, last_word)
            return None
        except BaseException as be:
            __print_error_discharge_driver(be, last_word)
            return None

    return wrapper

def __print_error_discharge_driver(exception,
                                 text: str = ""):
    print(f"An error | exception occurred: {exception}")
    input(text)
    Driver.CURRENT_INSTANCE.discharge()
