import sys
from collections import Counter
from typing import Callable

import os
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
        # count assertions per line
        self.assert_counter = Counter()
        self.tc_name = sys._getframe(1).f_code.co_name
        # the frame and code objects also offer other useful information:
        module_path = sys._getframe(1).f_code.co_filename
        self.mod_name = os.path.splitext(os.path.basename(module_path))[0]
        self.report: bool = kwargs.get('report', False)
        self.start_config: dict = kwargs.get('start_config', TestCase.default_start_config)
        self.start_func: Callable = kwargs.get('start_func', self.start_app)
        self.init_func: Callable = kwargs.get('init_func', self.init_app)
        self.priority: int = kwargs.get('prio', 2)
        self.start_ok = True
        self.init_ok = True
        # max number of assertions from same line number
        self.max_assert_count_per_line: int = kwargs.get('max_assert_count', 0)
        # mandatory app start with config
        if self.start_func is not None:
            self.start_ok = self.assert_true(self.start_app(), 'Failed to start')

        # optional test case init
        if self.init_func is not None:
            self.init_ok = self.assert_true(self.init_func(), 'Failed to init')
        else:
            print(f'{self.tc_name}: Init disabled')

    def is_test_ok(self) -> bool:
        return self.start_ok and self.init_ok

    def error(self) -> bool:
        return not self.start_ok or not self.init_ok

    def start_app(self) -> bool:
        print(f'{self.tc_name}: Start application with config:')
        for k, v in self.start_config.items():
            print(f'\t{k}={v}')
        return True

    def init_app(self) -> bool:
        self.assert_true(False, f'Test case init failed')
        return True

    def assert_false(self, condition: bool, fail_message: str, *, prio: int = None, report=None) -> bool:
        return self.assert_true(not condition, fail_message, prio=prio, report=report, frame=2)

    def assert_true(self, condition: bool, fail_message: str, *, prio: int = None, report=None, frame: int = 1) -> bool:
        if condition:
            return True
        # handle failed assertion
        # track assertion line number to avoid duplicates (e.g.: loops)
        line_number = sys._getframe(frame).f_lineno
        self.assert_counter[line_number] += 1
        # assert priority overrides test case priority
        priority = self.priority if prio is None else prio
        self.log_error(line_number, self.assert_counter[line_number], priority, fail_message)
        # assert report overrides test case report
        create_report = self.report if report is None else report
        # report assert failure to Jira
        if create_report and self.assert_counter[line_number] <= self.max_assert_count_per_line:
            if key := self.report_error(line_number, self.assert_counter[line_number], priority, fail_message):
                print(f'\tError reported as {key}')
            else:
                print('Error report failed, invalid Jira key returned')
        else:
            print('\tReport: disabled or max. counter exceeded')
        return False

    def create_assert_summary(self):
        print(f'Test case summary:\nTotal assertions failed: {sum(self.assert_counter.values())}')
        for line, count in self.assert_counter.items():
            print(f'\tLine {line}: {count}')

    def log_error(self, line_number: int, count: int, priority: int, fail_message: str):
        print(
            f'{self.tc_name} (line {line_number}, count {count}, prio={priority}): Assert failed with message "{fail_message}"')

    def report_error(self, line_number: int, count: int, priority: int, fail_message: str) -> str:
        host_name = socket.gethostname().upper()
        print(
            f'Error Report:\n\tHost: {host_name}\n\tModule: {self.mod_name}\n\tTest Case: {self.tc_name} (line {line_number}, count {count})\n\tPriority: {priority}\n\tMessage: {fail_message}')
        report_key = random.randint(1, 1000)
        return f'LST-{report_key}'
