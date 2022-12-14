from TestCase import TestCase
from report import report_error
from app import start_app

def test_case_init() -> bool:
    print(f'Test case init done')
    return True

def test_case_1():
    start_config = dict(
        tree='default_hw_tree',
        mic=None,
        sted=False,
        sim=True,
        release=True,
        force=False,
    )
    tc = TestCase(__name__, report_func=report_error, setup_func=start_app, setup_config=start_config, init_func=test_case_init, prio=1)
    if not tc.setup():
        return
    tc.assert_test(19 == 19, f'Test failed')
    tc.assert_test(1 == 0, f'Test failed')

def test_case_2():
    start_config = dict(
        force=True,
    )
    tc = TestCase(__name__, report_func=report_error, setup_func=start_app, setup_config=start_config, init_func=None, prio=2)
    if not tc.setup():
        return
    tc.assert_test(19 == 19, f'Test failed')
    tc.assert_test(1 == 0, f'Test failed')

