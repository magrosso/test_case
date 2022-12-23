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
        # start and init app
        self.start_config: dict = kwargs.get('start_config', TestCase.DEFAULT_START_CONFIG)
        self.start_app: Callable = kwargs.get('start', self.start_app)
        self.init_app: Callable = kwargs.get('init', self.init_app)
        self.priority: int = kwargs.get('prio', 2)

    def __enter__(self):
        # start app with config
        if self.start_app is not None:
            if not self.assert_true(self.start_app(), 'Failed to start app'):
                return None

        # optional test case init
        if self.init_app is not None:
            if not self.assert_true(self.init_app(), 'Failed to init app'):
                return None

        return self

    def __exit__(self, type, value, traceback):
        # exception occurred in with-block
        if type is AttributeError:
            print(f'__exit__: Exception in "with" block: skipping test case')

        # no exception - just report all the test case errors
        # report assert failure to Jira
        if self.report:
            if key := self.report_error():
                print(f'\tError reported as {key}')
            else:
                print('Error report failed, invalid Jira key returned')
        return True  # don't raise again

    def start_app(self) -> bool:
        print(f'{self.tc_name}: Start application with config:')
        for k, v in self.start_config.items():
            print(f'\t{k}={v}')
        return True

    def init_app(self) -> bool:
        return self.assert_true(False, f'Test case init failed')

    def assert_false(self, condition: bool, fail_message: str, *, prio: int = None, report=None) -> bool:
        line_number = sys._getframe(1).f_lineno
        return self.assert_true(not condition, fail_message, 'False', line_number, prio=prio, report=report)

    def assert_equal(self, num_1: int, num_2: int, fail_message: str, *, prio: int = None, report=None) -> bool:
        line_number = sys._getframe(1).f_lineno
        return self.assert_true(num_1 == num_2, fail_message, 'Equal', line_number, prio=prio, report=report)

    def assert_true(self, condition: bool, fail_message: str, prefix: str = 'True', line_number: int = None, *,
                    prio: int = None,
                    report: bool = None,
                    log: bool = True) -> bool:
        if condition:
            return True
        # handle failed assertion
        # track assertion line number to avoid duplicates (e.g.: loops)
        line_number = sys._getframe(1).f_lineno if line_number is None else line_number
        # assert priority overrides test case priority
        priority = self.priority if prio is None else prio
        add_to_report = self.report and (report is None or report)
        if add_to_report:
            self.assert_fail_list.append(f'Line {line_number} (prio={priority}): "{fail_message}"')

        create_log = self.log and (log is None or log)
        if create_log:
            self.log_error(line_number, priority, fail_message, prefix)
            
        return False

    def log_error(self, line_number: int, priority: int, fail_message: str, prefix: str):
        print(
            f'LOG: {self.mod_name}:{self.tc_name}:{line_number} (prio={priority}): not {prefix}: "{fail_message}"')

    def report_error(self) -> str:
        print(f'Test case error report summary:')
        host_name = socket.gethostname().upper()
        print(f'\tHost: {host_name}\n\tModule: {self.mod_name}\n\tTest Case: {self.tc_name}')
        for assert_failure in self.assert_fail_list:
            print(f'\t{assert_failure}')
        report_key = random.randint(1, 1000)
        return f'LST-{report_key}'
