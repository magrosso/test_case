import sys
from typing import Callable


class TestCase:
    def __init__(self, mod_name: str, report_func: Callable, setup_func: Callable, setup_config: dict):
        """
        """
        self.tc_name = sys._getframe(1).f_code.co_name
        self.mod_name = mod_name
        self.report_func: Callable = report_func
        self.setup_func: Callable = setup_func
        self.setup_config: dict = setup_config
        self.reports: list = []
        print(f'\nCreated: "{self.tc_name}"')

    def list_reports(self):
        for num, report in enumerate(self.reports, 1):
            print(f'{num}. Report: {report}')

    def setup(self) -> bool:
        # call setup to start application with configuration defined
        if self.setup_config is not None:
            return self.setup_func(self.setup_config)
        else:
            print('\tSetup: disabled')
        return True

    def assert_test(self, cond: bool, fail_message: str) -> bool:
        if not cond:
            print(f'\tfail_message')
            if self.report_func is not None:
                if key := self.report_func(self.mod_name, self.tc_name):
                    self.reports.append(key)
                    print(f'\tError reported as {key}')
                else:
                    print(f'Error report failed')
            else:
                print('\tReport: disabled')
        return cond

