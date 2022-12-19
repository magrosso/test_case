import sys
import os
from collections import Counter
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
        # count assertions per line
        self._assert_fail_counter = Counter()
        self._tc_name = sys._getframe(1).f_code.co_name
        # the frame and code objects also offer other useful information:
        mod_path = sys._getframe(1).f_code.co_filename
        self._mod_name: str = os.path.splitext(os.path.basename(mod_path))[0]
        self._report: bool = kwargs.get('report', False)
        self.start_config: dict = kwargs.get('start_config', TestCase.default_start_config)
        self._start_func: Callable = kwargs.get('start', self.start_app)
        self._init_func: Callable = kwargs.get('init', self.init_app)
        self._priority: int = kwargs.get('prio', 2)
        # max number of assertions from same line number
        self.max_assert_count_per_line: int = kwargs.get('max_assert_count', 1)
        print(f'\nCreated: "{self._tc_name}"')
        self._start_fail = False
        if self._start_func is not None:
            if self._start_func():
                print(f'{self._tc_name}: Started')
            else:
                self._start_fail = True
                print(f'{self._tc_name}: Start failed')
        # optional test case init
        self._init_fail = False
        if self._init_func is not None:
            if self._init_func():
                print(f'{self._tc_name}: Initialized')
            else:
                self._init_fail = True
                print(f'{self._tc_name}: Init failed')
        else:
            print(f'{self._tc_name}: Init disabled')

    def start_app(self) -> bool:
        print(f'{self._tc_name}: Start application with config:')
        for k, v in self.start_config.items():
            print(f'\t{k}={v}')
        self.assert_true(True, f'Test start failed')
        return self.assert_true(False, f'Test start failed', frame=2)

    def init_app(self) -> bool:
        self.assert_true(True, f'Test case init failed')
        return self.assert_true(False, f'Test case init failed', frame=2)

    def assert_false(self, condition: bool, fail_message: str, *, prio: int = None, report=None) -> bool:
        return self.assert_true(not condition, fail_message, prio=prio, report=report, frame=2)

    def assert_true(self, condition: bool, fail_message: str, *, prio: int = None, report=None, frame: int = 1) -> bool:
        # handle failed assertion
        if condition:
            return True
        # track assertion line number to avoid duplicates (e.g.: loops)
        line_number = sys._getframe(frame).f_lineno
        self._assert_fail_counter[line_number] += 1
        # assert priority overrides test case priority
        priority = self._priority if prio is None else prio
        self.log_error(line_number, self._assert_fail_counter[line_number], priority, fail_message)
        # assert report overrides test case report
        create_report = self._report if report is None else report
        # report assert failure to Jira
        if create_report and self._assert_fail_counter[line_number] <= self.max_assert_count_per_line:
            if key := self.report_error(line_number, self._assert_fail_counter[line_number], priority, fail_message):
                print(f'\tError reported as {key}')
            else:
                print(f'Error report failed, invalid Jira key returned')
        else:
            print('\tReport: disabled or max. counter exceeded')
        return False

    def create_assert_summary(self):
        print(f'Test case summary for {self._mod_name}:{self._tc_name}:\nTotal assertions failed: {sum(self._assert_fail_counter.values())}')
        for line, count in self._assert_fail_counter.items():
            print(f'\t{line}: {count}')

    def log_error(self, line_number: int, count: int, priority: int, fail_message: str):
        print(f'{self._mod_name}:{self._tc_name}:{line_number} (count {count}, prio={priority}): Assert failed with message "{fail_message}"')

    def report_error(self, line_number: int, count: int, priority: int, fail_message: str) -> str:
        host_name = socket.gethostname().upper()
        print(
            f'Error Report:\n\tHost: {host_name}\n\tModule: {self._mod_name}\n\tTest Case: {self._tc_name} (line {line_number}, count {count})\n\tPriority: {priority}\n\tMessage: {fail_message}')
        report_key = random.randint(1, 1000)
        return f'LST-{report_key}'

    @property
    def priority(self):
        return self._priority

    @property
    def mod_name(self):
        return self._mod_name

    @property
    def name(self):
        return self._tc_name

    @property
    def init_fail(self):
        return self._init_fail

    @property
    def start_fail(self):
        return self._start_fail

    @property
    def fail(self):
        return self._init_fail or self._start_fail
