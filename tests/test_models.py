import datetime

import pytest

from api.models import PolicyType
from api.models import Breed
from api.models import DuplicateError


@pytest.mark.parametrize(
    ('name', 'base_price'),
    [
        ('', 800),
        (None, 800),
        ('annual', 0),
        ('annual', -1),
        ('annual', 'free?'),
    ]
)
def test_invalid_policy_add_data(log, db, name, base_price):
    with pytest.raises(ValueError):
        PolicyType.add(name, base_price)


def test_basic_policy_operations(log, db):
    """Test storage layer logic add/get/etc for PolicyType.
    """
    # check the empty state doesn't break things
    assert PolicyType.policies() == []

    # there should be no annual policy in there:
    PolicyType.get('annual') is not None

    # check the basic error cases
    #
    # no name given or its empty:
    with pytest.raises(ValueError):
        PolicyType.add(None, 10)

    with pytest.raises(ValueError):
        PolicyType.add('annual', 0)

    with pytest.raises(ValueError):
        PolicyType.add('annual', -1)

    # Add in a policy (price is in pence)
    PolicyType.add('annual', 800)
    assert len(PolicyType.policies()) == 1
    policy = PolicyType.get('annual')
    assert policy is not None
    assert policy.name == 'annual'
    assert policy.base_price == 800
    assert policy.created is not None

    # The policy type is unique so adding again should error
    with pytest.raises(DuplicateError):
        PolicyType.add('annual', 1050)


@pytest.mark.parametrize(
    ('species', 'name', 'risk_gradient'),
    [
        (None, 'border_collie', 1),
        ('', 'border_collie', 1),
        ('dog', None, 1),
        ('dog', '', 1),
        ('dog', 'border_collie', 0),
        ('dog', 'border_collie', -1),
        ('dog', 'border_collie', 'sheep?'),
    ]
)
def test_invalid_breed_add_data(log, db, species, name, risk_gradient):
    with pytest.raises(ValueError):
        Breed.add('dot', None, 2)


def test_basic_policy_operations(log, db):
    """Test storage layer logic add/get/etc for Breed.
    """
    # check the empty state doesn't break things
    assert Breed.breeds() == []

    # there should be no border_collie in there:
    Breed.get('dog', 'border_collie') is not None

    # Add in a policy (price is in pence)
    Breed.add('dog', 'border_collie', 2)

    assert len(Breed.breeds()) == 1

    breed = Breed.get('dog', 'border_collie')
    assert breed is not None
    assert breed.species == 'dog'
    assert breed.name == 'border_collie'
    assert breed.risk_gradient == 2
    assert breed.created is not None
