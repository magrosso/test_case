import sys
from typing import Callable


class TestCase:
    def __init__(self, mod_name: str, report_func: Callable, setup_func: Callable, setup_config: dict, init_func: Callable, prio: int):
        """
        """
        self.tc_name = sys._getframe(1).f_code.co_name
        self.mod_name = mod_name
        self.report_func: Callable = report_func
        self.setup_func: Callable = setup_func
        self.setup_config: dict = setup_config
        self.init_func: Callable = init_func
        self.priority: int = prio
        print(f'\nCreated: "{self.tc_name}"')

    def setup(self) -> bool:
        # call setup to start application with configuration defined

        if self.setup_func is not None and self.setup_config is not None:
            setup_ok = self.setup_func(self.setup_config)
        else:
            print('\tSetup: disabled')
            setup_ok = True

        if setup_ok:
            if self.init_func is not None:
                setup_ok = self.init_func()
            else:
                print('\tInit: disabled')
        return setup_ok
    def assert_test(self, cond: bool, fail_message: str) -> bool:
        if not cond:
            print(f'Assert in "{self.tc_name}" failed with message "{fail_message}", priority={self.priority}')
            if self.report_func is not None:
                if key := self.report_func(self.mod_name, self.tc_name, self.priority):
                    print(f'\tError reported as {key}')
                else:
                    print(f'Error report failed')
            else:
                print('\tReport: disabled')
        return cond

