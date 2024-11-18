import functools

from classes.navigator import Navigator


def handle_exceptions_quit_driver(func):
    """Декоратор для обработки исключений."""
    @functools.wraps(func)  # Сохраняем метаданные оригинальной функции
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Произошла ошибка: {e}")  # или логирование в файл
            # Можно добавить дополнительную обработку ошибки, например, возврат значения по умолчанию
            navigator = Navigator()
            driver = navigator.get_driver_obj()
            driver.discharge()
            return None  # или поднять исключение снова: raise e

    return wrapper
