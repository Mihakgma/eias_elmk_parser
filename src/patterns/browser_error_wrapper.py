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
            __print_error_discharge_driver(exception=e,
                                           function=func,
                                           text=last_word)
            return None
        except WebDriverException as wde:
            __print_error_discharge_driver(exception=wde,
                                           function=func,
                                           text=last_word)
            return None
        except TypeError as te:
            __print_error_discharge_driver(exception=te,
                                           function=func,
                                           text=last_word)
            return None
        except BaseException as be:
            __print_error_discharge_driver(exception=be,
                                           function=func,
                                           text=last_word)
            return None

    return wrapper


def __print_error_discharge_driver(exception,
                                   function,
                                   text: str = "",
                                   traceback: bool = True):
    print(f"An error | exception occurred: {exception}")
    print(f"<{function.__name__}> function has been crashed on ...")
    if traceback:
        tb_lines = traceback.extract_stack()
        for line in tb_lines:
            if function.__name__ in line.filename:
                print(f" {line.filename}:{line.lineno} in {line.funcName} ({line.line})")
    input(text)
    Driver.CURRENT_INSTANCE.discharge()
