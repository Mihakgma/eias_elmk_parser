from driver import Driver
from injector import Injector
from navigator import Navigator


class InjectManager:
    @staticmethod
    def do_inject(driver: Driver,
                  navigator: Navigator,
                  auto_charge: bool = True):
        injector = Injector(driver=driver,
                            navigator=navigator,
                            auto_charging=auto_charge)
        injector.inject()
