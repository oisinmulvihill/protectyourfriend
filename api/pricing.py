"""
This logic determines how the policy price is worked out based on the given
customer data and our own information.

Pricing is handle in pence. The makes it much easier to deal with.

"""
import logging


def calculate_age_risk(risk_gradient, age, multiplier=100):
    """Get the extra added to the price for given breed risk gradient & age.

    :param risk_gradient: The breed risk gradient integer.

    If this is not a number or a number greater than 0 ValueError will be
    raised.

    :param age: The current pet's age.

    If this is not a number, then ValueError will be raised.

    :param multiplier: The pence amount  current pet's age.

    I'm using a simple straight line model to approxiate how age increases the
    risk. I use the slope of a line formula y = mx + c for this. C is set 0 in
    this case. The risk_gradient is used for m and the age represents the x
    axis. I then use an the multiplier to get the pence amount to add to the
    policy.

    E.g.:

    breed_risk: 3
    age: 10
    multiplier: 100

    y = (3)(10) = 30
    price = (30)(100) = 3000

    :returns: The pence amount to add to the policy.

    """
    # validate inputs ready for calulations:
    if risk_gradient is None:
        raise ValueError("The risk_gradient is not a number!")

    risk = int(risk_gradient)
    if risk < 1:
        raise ValueError("The risk_gradient must be greater than zero!")

    if age is None:
        raise ValueError("The age is not a number!")

    _age = int(age)
    if _age < 0:
        raise ValueError("The age must be 0 or more!")

    if multiplier is None:
        raise ValueError("The age is not a number!")

    _multiplier = int(multiplier)
    if _multiplier < 1:
        raise ValueError("The multiplier must be 1 or more!")

    return (risk * _age * _multiplier)


def excess_reduction(price, excess, max_excess=100000):
    """Work out how much to reduce the price the policy price by.

    I'm going to start out and assume a discount of 0 - 20% of the price.

    :param price: The current policy amount in pence.

    :param excess: The excess amount in pence.

    :param max_excess: The max discount in pence.

    If the excess is > max_excess we just give 20% discount.

    :returns: An integer percentage discount to give.

    """
    log = logging.getLogger(__name__)

    log.debug(f"price:{price} excess:{excess} max_excess:{max_excess}")

    _excess = int(excess)
    if _excess < 0:
        log.warn(
            f"For price '{price}' with excess '{excess}' no discount was "
            "given! The excess must be greater or equal to 0!"
        )
        return price

    if _excess > max_excess:
        # max 20% discount
        returned = price - (price * 0.2)

    else:
        # work out a discount from 0 - 20% on the price:
        discount = 20 * (excess / max_excess)
        returned = price - discount

    log.debug(
        f"price:{price} excess:{excess} max_excess:{max_excess} "
        f"reduction: {returned}"
    )

    return returned


def generate_price(base_price, risk_gradient, age, excess, max_excess):
    """
    """
