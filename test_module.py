from TestCase import TestCase


def test_case_1():
    start_config = dict(
        tree='default_hw_tree',
        mic=None,
        sted=False,
        sim=True,
        release=True,
        force=False,
    )
    tc = TestCase(report_func=None, start_func=None, start_config=start_config, prio=1)
    tc.assert_test(19 == 19, f'Test failed', 3)
    tc.assert_test(1 == 0, f'Test failed', 4)


def test_case_2():
    tc = TestCase(start_config={'tree': 'other_tree'})
    tc.assert_test(19 == 19, f'Test failed')
    tc.assert_test(1 == 0, f'Test failed')
