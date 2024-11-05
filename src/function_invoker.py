class Invoker:
    def __init__(self, obj: object, func_name: str) -> None:
        self.__obj = obj
        self.__func_name = func_name

    def __call__(self, *args, **kwargs):
        func_name = self.__func_name
        obj = self.__obj
        try:
            func = getattr(obj, func_name)
            return func(*args, **kwargs)
        except TypeError:
            print(f'{func_name} is not callable')
        except AttributeError:
            print(f'{func_name} does not exist in {obj}')


class SomeClass(object):
    def __init__(self):
        pass

    def do_something(self):
        print("I am a method")


if __name__ == '__main__':
    some_obj = SomeClass()
    invoker = Invoker(some_obj, 'do_something')
    invoker()
