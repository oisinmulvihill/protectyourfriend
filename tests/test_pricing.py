"""
Verify the policy pricing 'engine'.

"""
import pytest

from api import pricing
from api.models import PolicyType
from api.models import Breed



@pytest.mark.parametrize(
    ('risk_gradient', 'age', 'multiplier'),
    [
        # Bad data resulting in ValueError
        #
        # risk not valid
        (0, 4, 100),
        ('', 4, 100),
        (None, 4, 100),
        # age not valid
        (1, -1, 100),
        (1, '', 100),
        (1, None, 100),
        # multiplier not valid
        (1, 1, 0),
        (1, 1, -1),
        (1, 1, ''),
        (1, 1, None),
    ]
)
def test_invalid_calculate_age_risk_data(
    log, risk_gradient, age, multiplier
):
    with pytest.raises(ValueError):
        pricing.calculate_age_risk(risk_gradient, age, multiplier)


@pytest.mark.parametrize(
    ('risk_gradient', 'age', 'multiplier', 'expected'),
    [
        # OK cases
        #
        # low risk breed: 1 * 1 * 100
        (1, 1, 100, 100),
        # higher risk breed
        (1, 1, 100, 100),
        (2, 1, 100, 200),
        (3, 1, 100, 300),
        # more risky as animal ages
        (1, 5, 100, 500),
        (2, 5, 100, 1000),
        (3, 5, 100, 1500),
        (3, 15, 100, 4500),
    ]
)
def test_calcualte_age_risk(
    log, risk_gradient, age, multiplier, expected
):
    """Verify how age_risk price is calculated.
    """
    assert pricing.calculate_age_risk(
        risk_gradient, age, multiplier
    ) == expected


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
        # Other amounts:
        (100, 500, 1000, 90),
        (100, 250, 1000, 95),
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


@pytest.mark.parametrize(
    (
        'base_price', 'risk_gradient', 'age', 'excess', 'expected'
    ),
    [
        # with default multiplier this should be: 1000 * (1 * 1 * 10)
        (1000, 1, 1, 0, 10000),
        # with discount for excess this should be:
        (1000, 1, 1, pricing.MAX_EXCESS_GIVEN, 990),
    ]
)
def test_price_quote_generation(
    log, base_price, risk_gradient, age, excess, expected
):
    """Verify the price for a quote.
    """
    assert pricing.generate_price(
        base_price,
        risk_gradient,
        age,
        excess,
    ) == expected