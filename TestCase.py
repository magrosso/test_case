import sys
from typing import Callable

import socket
import random

# todo: handle test case dependencies on hardware config
class TestCase:
    default_start_config = dict(
        tree='default_hw_tree',
        mic=None,
        sted=False,
        sim=True,
        release=True,
        force=False,
    )

    def __init__(self, **kwargs):
        """
        """
        self.tc_name = sys._getframe(1).f_code.co_name
        # the frame and code objects also offer other useful information:
        self.mod_name = sys._getframe(1).f_code.co_filename
        self.report_func: Callable = kwargs.get('report_func', self.report_error)
        self.start_config: dict = kwargs.get('start_config', TestCase.default_start_config)
        # todo: is there a default for init?
        self.init_func: Callable = kwargs.get('init_func', self.test_case_init)
        self.priority: int = kwargs.get('prio', 2)
        print(f'\nCreated: "{self.tc_name}"')
        # mandatory app start with config
        if self.start_app():
            print(f'{self.tc_name}: Started')
        else:
            print(f'{self.tc_name}: Start failed')
        # optional test case init
        if self.init_func is not None:
            if self.init_func():
                print(f'{self.tc_name}: Initialized')
            else:
                print(f'{self.tc_name}: Init failed')
        else:
            print(f'{self.tc_name}: Init disabled')

    def start_app(self) -> bool:
        print(f'{self.tc_name}: Start application with config:')
        for k, v in self.start_config.items():
            print(f'\t{k}={v}')
        return True

    def test_case_init(self) -> bool:
        if not self.assert_test(self.tc_name == 'test_case_1', f'Test case name mismatch'):
            return False
        return True

    def assert_test(self, cond: bool, fail_message: str, assert_prio: int = None) -> bool:
        if not cond:
            # assert priority overrides test case priority
            priority = self.priority if assert_prio is None else assert_prio
            line_number = sys._getframe(1).f_lineno
            print(f'{self.tc_name} (line {line_number}): Assert failed with message "{fail_message}", priority={priority}')
            # report assert fail
            if self.report_func is not None:
                if key := self.report_func():
                    print(f'\tError reported as {key}')
                else:
                    print(f'Error report failed, invalid Jira key returned')
            else:
                print('\tReport: disabled')
        return cond

    def report_error(self) -> str:
        host_name = socket.gethostname().upper()
        print(f'Report:\n\tHost: {host_name}\n\tModule: {self.mod_name}\n\tTest Case: {self.tc_name}\n\tPriority: {self.priority}')
        report_key = random.randint(1, 1000)
        return f'LST-{report_key}'

