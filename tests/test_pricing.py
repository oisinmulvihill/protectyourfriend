"""
Verify the policy pricing 'engine'.

"""
import pytest

from api import pricing


@pytest.mark.parametrize(
    ('policy_price', 'excess', 'max_excess', 'expected'),
    [
        # Bad data resulting in no discount to the policy
        (100, 0, 100000, 100),
        (100, -1, 100000, 100),

        # OK cases
        #
        # Pay the max excess for 20% discount:
        (100, 100000, 100000, 80),
        # offering to pay more than excess gives no further discount:
        (100, 200000, 100000, 80),
        #
        (100, 500, 1000, 90),
    ]
)
def test_excess_reduction_pricing(
    log, policy_price, excess, max_excess, expected
):
    """Verify how excess modify the given policy price.
    """
    assert pricing.excess_reduction(
        policy_price, excess, max_excess
    ) == expected
