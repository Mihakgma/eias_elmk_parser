from threading import Thread


def thread(func):
    """
    Это простейший декоратор. В него мы будем заворачивать
    функции. Любая функция, завернутая этим декоратором,
    будет выполнена в отдельном потоке.
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        current_thread = Thread(
            target=func, args=args, kwargs=kwargs)
        current_thread.start()

    return wrapper
