from TestCase import TestCase


def init_test_case_1() -> bool:
    print('called: init_test_case_1')
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

    with TestCase(report=True, start_config=start_config, prio=1, init=lambda: False, start=lambda: True) as tc:
        tc.assert_true(19 == 18, f'Test case failed', prio=3)
        for repeat in range(2):
            tc.assert_true(1 == 0, f'Test case failed', prio=4, report=False, log=False)
        tc.assert_true(19 == 18, f'Test case failed', prio=3)
        tc.assert_false(12 == 12, f'12 == 12 not false')

    print('after with-block')


def test_case_2():
    with TestCase(log=True, report=True, start_config={'tree': 'other_tree'}, init=lambda: True, start=lambda:False) as tc:
        tc.assert_false(19 == 19, f'Test case failed: 19 == 19')
        tc.assert_true(1 == 0, f'Test case failed', report=True, log=True)

    print('after with-block')
