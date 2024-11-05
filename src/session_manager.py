from singleton import Singleton


class SessionManager(Singleton):
    __SESSIONS_CREATED = []

    def __init__(self):
        self.__current_session = None


if __name__ == '__main__':
    pass
