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

    with TestCase(report=True, start_config=start_config, prio=1, init=lambda: True, start=lambda: True) as tc:
        tc.assert_true(19 == 18, f'19==18', prio=3)
        for repeat in range(2):
            tc.assert_true(1 == 0, f'1==0', prio=4, report=False, log=False)

        tc.assert_equal(9, 9, f'9,9', prio=1)
        tc.assert_equal(9, 8, f'9,8', prio=1)
        tc.assert_true(19 == 18, f'19==18', prio=3)
        tc.assert_false(12 == 12, f'12 == 12')

    print('after with-block')


def test_case_2():
    with TestCase(log=True, report=True, start_config={'tree': 'other_tree'}, init=lambda: True, start=lambda:True) as tc:
        tc.assert_false(19 == 19, f'19 == 19')
        tc.assert_true(1 == 0, f'1==0', report=True, log=True)

    print('after with-block')
