import os
import functools

def setter_log(filepath):
    """
    Decor for recording seterror logs.

    Args:
        filepath: path to dir with seterror logs.
    """

    def decorator(setter_method):
        @functools.wraps(setter_method)
        def wrapper(self, value):
            method_name = setter_method.__name__
            if method_name.startswith("set_"):
                filename = method_name[4:] + ".txt"
                full_path = os.path.join(filepath, filename)
                if not os.path.exists(filepath):
                    try:
                        os.makedirs(filepath)
                        print(f"Dir '{filepath}' created.")
                    except OSError as e:
                        print(f"Error while trying to create '{filepath}': {e}")
                        return setter_method(self, value)

                try:
                    with open(full_path, 'w') as f:
                        f.write(str(value))
                except OSError as e:
                    print(f"Error writing to file {full_path}: {e}")

            return setter_method(self, value)
        return wrapper
    return decorator


class MyClass:
    def __init__(self):
        self._name = ""
        self._age = 0

    @setter_log("logs")
    def set_name(self, value):
        self._name = value

    @setter_log("logs")
    def set_age(self, value):
        self._age = value


if __name__ == "__main__":
    my_instance = MyClass()
    my_instance.set_name("Иван")
    my_instance.set_age(30)

    print(os.path.exists("logs/name.txt"))  # True
    print(os.path.exists("logs/age.txt"))  # True

    with open("logs/name.txt", "r") as f:
        print(f.read())

    with open("logs/age.txt", "r") as f:
        print(f.read())
