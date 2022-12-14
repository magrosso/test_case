from TestCase import TestCase
from report import report_error
from app import start_app


def test_case_report_on():
    start_config = dict(
        tree='default_hw_tree',
        mic=None,
        sted=False,
        sim=True,
        release=True,
        force=False,
    )
    tc = TestCase(__name__, report_func=report_error, setup_func=start_app, setup_config=start_config)
    if not tc.setup():
        return
    tc.assert_test(19 == 19, f'Test failed')
    tc.assert_test(1 == 0, f'Test failed')
    tc.list_reports()

def test_case_report_off():
    start_config = dict(
        force=True,
    )
    tc = TestCase(__name__, report_func=None, setup_func=start_app, setup_config=start_config)
    if not tc.setup():
        return
    tc.assert_test(19 == 19, f'Test failed')
    tc.assert_test(1 == 0, f'Test failed')

