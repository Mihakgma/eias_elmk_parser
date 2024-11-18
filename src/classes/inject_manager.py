# import session_manager
from classes.driver import Driver
from injector import Injector
from navigator import Navigator


class InjectManager:
    @staticmethod
    def do_inject(driver: Driver,
                  navigator: Navigator,
                  session_manager,
                  auto_charge: bool = True,
                  test_charge: bool = True):
        injector = Injector(driver=driver,
                            navigator=navigator,
                            session_manager=session_manager,
                            auto_charging=auto_charge)
        injector.inject(test_charge)
