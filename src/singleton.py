class Singleton:
    __INSTANCE = None

    def __new__(cls, *args, **kwargs):
        # cannot create an object of the current class
        if cls == Singleton:
            return
        if cls.__INSTANCE is None:
            print("new Singleton instance has been created")
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE


class SomeClass(Singleton):
    pass


if __name__ == '__main__':
    obj1 = SomeClass()
    obj2 = SomeClass()
    print(obj1 == obj2)
    singleton = Singleton()
    print(singleton)
