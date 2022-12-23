import sys
from collections import Counter
from typing import Callable

import os
import socket
import random


# todo: handle test case dependencies on hardware config
class TestCase:
    DEFAULT_START_CONFIG = dict(
        tree='default_hw_tree',
        mic=None,
        sted=False,
        sim=True,
        release=True,
        force=False,
    )

    def __init__(self, **kwargs):
        # count assertions per line
        self.assert_fail_list = list()
        self.tc_name: str = sys._getframe(1).f_code.co_name
        # the frame and code objects also offer other useful information:
        module_path: str = sys._getframe(1).f_code.co_filename
        self.mod_name: str = os.path.splitext(os.path.basename(module_path))[0]
        # report or log failed assertions?
        self.report: bool = kwargs.get('report', False)
        self.log: bool = kwargs.get('log', True)

        self.start_config: dict = kwargs.get('start_config', TestCase.DEFAULT_START_CONFIG)
        self.start_func: Callable = kwargs.get('start_func', self.start_app)
        self.init_func: Callable = kwargs.get('init_func', self.init_app)
        self.priority: int = kwargs.get('prio', 2)
        self.start_fail = False
        self.init_fail = False
        # max number of assertions from same line number
        self.max_assert_count_per_line: int = kwargs.get('max_assert_count', 0)
        # mandatory app start with config
        if self.start_func is not None:
            self.start_fail = not self.assert_true(self.start_app(), 'Failed to start')

        # optional test case init
        if self.init_func is not None:
            self.init_fail = not self.assert_true(self.init_func(), 'Failed to init')
        else:
            print(f'{self.tc_name}: Init disabled')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Create a summary report of all failed assertions

        Args:
            type ():
            value ():
            traceback ():

        Returns:

        """
        # re-raise exception
        if type is not None:
            return False

        # no exception - just report all the test case errors
        # report assert failure to Jira
        if self.report:
            if key := self.report_error():
                print(f'\tError reported as {key}')
            else:
                print('Error report failed, invalid Jira key returned')
        return True

    @property
    def fail(self) -> bool:
        return self.start_fail or self.init_fail

    def start_app(self) -> bool:
        print(f'{self.tc_name}: Start application with config:')
        for k, v in self.start_config.items():
            print(f'\t{k}={v}')
        return True

    def init_app(self) -> bool:
        self.assert_true(False, f'Test case init failed')
        return True

    def assert_false(self, condition: bool, fail_message: str, *, prio: int = None, report=None) -> bool:
        line_number = sys._getframe(1).f_lineno
        return self.assert_true(not condition, fail_message, line_number, prio=prio, report=report)

    def assert_true(self, condition: bool, fail_message: str, line_number: int = 0, *, prio: int = None, report: bool = None,
                    log: bool = True) -> bool:
        if condition:
            return True
        # handle failed assertion
        # track assertion line number to avoid duplicates (e.g.: loops)
        line_number = sys._getframe(1).f_lineno if line_number == 0 else line_number
        # assert priority overrides test case priority
        priority = self.priority if prio is None else prio
        add_to_report = self.report and (report is None or report)
        if add_to_report:
            self.assert_fail_list.append(f'Line {line_number} (prio={priority}): "{fail_message}"')

        add_to_log = self.log and (log is None or log)
        if add_to_log:
            self.log_error(line_number, priority, fail_message)
        return False

    def log_error(self, line_number: int, priority: int, fail_message: str):
        print(
            f'{self.mod_name}:{self.tc_name}:{line_number} (prio={priority}): Assert failed: "{fail_message}"')

    def report_error(self) -> str:
        print(f'Test case error report summary:')
        host_name = socket.gethostname().upper()
        print(f'\tHost: {host_name}\n\tModule: {self.mod_name}\n\tTest Case: {self.tc_name}')
        for assert_failure in self.assert_fail_list:
            print(f'\t{assert_failure}')
        report_key = random.randint(1, 1000)
        return f'LST-{report_key}'
