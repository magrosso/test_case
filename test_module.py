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
    tc = TestCase(report=False, start_config=start_config, prio=1, max_assert_count=1)
    if tc.error():
        return

    tc.assert_true(19 == 18, f'Test case failed', prio=3, report=True)
    for repeat in range(1):
        tc.assert_true(1 == 0, f'Test case failed', prio=4, report=True)
    tc.assert_true(19 == 18, f'Test case failed', prio=3, report=True)
    tc.assert_false(12 == 12, f'12 == 12 not false')
    tc.create_assert_summary()


def test_case_2():
    tc = TestCase(start_config={'tree': 'other_tree'})
    if tc.error():
        return
    tc.assert_true(19 == 19, f'Test case failed')
    tc.assert_true(1 == 0, f'Test case failed', report=True)
    tc.create_assert_summary()
