import functools
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from traceback import extract_stack
from sys import exit as sys_exit

from classes.driver import Driver


def handle_exceptions_quit_driver(func):
    """Decorator for browser exceptions handling"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        last_word = "Press any key to close application..."
        try:
            return func(*args, **kwargs)
        except (NoSuchWindowException, WebDriverException, TypeError, BaseException) as e:
            __print_error_discharge_driver(exception=e,
                                           function=func,
                                           text=last_word,
                                           need_traceback=True)
            sys_exit(1)
    return wrapper


def __print_error_discharge_driver(exception,
                                   function,
                                   text: str = "",
                                   need_traceback: bool = True):
    last_driver = Driver.CURRENT_INSTANCE
    last_navigator = last_driver.get_linked_navigator()
    last_navigator.serialize()
    print(f"An error | exception occurred: {exception}")
    print(f"<{function.__name__}> function has been crashed on ...")
    if need_traceback:
        tb_lines = extract_stack()
        for line in reversed(tb_lines):  # Iterate in reverse order
            if function.__name__ in line.filename:
                print(f" {line.filename}:{line.lineno} in {line.name} ({line.line})")
                break  # Exit the loop after finding the relevant line
    input(text)
    last_driver.discharge()
