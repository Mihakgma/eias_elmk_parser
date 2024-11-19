import functools
from selenium.common.exceptions import NoSuchWindowException

from classes.driver import Driver


def handle_exceptions_quit_driver(func):
    """Decorator for browser exceptions handling"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoSuchWindowException as e:
            print(f"Произошла ошибка: {e}")
            Driver.CURRENT_INSTANCE.discharge()
            return None
        except TypeError as te:
            print(f"Произошла ошибка: {te}")
            Driver.CURRENT_INSTANCE.discharge()
            return None

    return wrapper
